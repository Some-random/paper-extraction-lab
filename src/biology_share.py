"""Design-based estimates from labelled, stratified random document samples.

Each shard must be sampled uniformly without replacement, independently of
other shards. Text labels are supplied by a reviewer, not inferred here. Token
counts refer to complete documents. Intervals describe sampling uncertainty;
they do not quantify classification errors or corpus duplication.
"""

from collections import defaultdict
from collections.abc import Mapping
import math
from numbers import Integral, Real


LABELS = ("biology", "clinical", "other", "mixed")
_Z95 = 1.959963984540054


def _number(value, field):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{field} must be a nonnegative finite number")
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{field} must be a nonnegative finite number")
    return value


def _interval(estimate, standard_error, upper=None):
    high = estimate + _Z95 * standard_error
    return [max(0.0, estimate - _Z95 * standard_error),
            min(upper, high) if upper is not None else high]


def _estimate(strata, numerator, denominator=None):
    """HT total and optional stratified ratio, including within-stratum FPC."""
    total, variance, denominator_total = 0.0, 0.0, 0.0
    for rows in strata.values():
        population, sample = rows[0]["shard_rows"], len(rows)
        values = [float(numerator(row)) for row in rows]
        mean = math.fsum(values) / sample
        total += population * mean
        if sample < population:
            sample_variance = math.fsum((value - mean) ** 2 for value in values) / (sample - 1)
            variance += population ** 2 * (1 - sample / population) * sample_variance / sample
        if denominator is not None:
            denominator_total += population * math.fsum(denominator(row) for row in rows) / sample
    se = math.sqrt(max(0.0, variance))
    result = {"estimate": total, "standard_error": se, "ci95": _interval(total, se)}
    if denominator is None:
        return result
    if denominator_total <= 0:
        raise ValueError("token-share denominator must be positive")
    share = total / denominator_total
    residual_variance = 0.0
    for rows in strata.values():
        population, sample = rows[0]["shard_rows"], len(rows)
        if sample == population:
            continue
        residuals = [numerator(row) - share * denominator(row) for row in rows]
        mean = math.fsum(residuals) / sample
        sample_variance = math.fsum((value - mean) ** 2 for value in residuals) / (sample - 1)
        residual_variance += population ** 2 * (1 - sample / population) * sample_variance / sample
    share_se = math.sqrt(max(0.0, residual_variance)) / denominator_total
    result.update(share=share, share_standard_error=share_se,
                  share_ci95=_interval(share, share_se, upper=1.0))
    return result


def estimate_biology_share(records, *, source_total_tokens=None, expected_sample_counts=None):
    """Return separate source/target-token estimates for each input corpus.

    Required record keys: ``corpus``, ``shard_id``, ``shard_rows``,
    ``source_tokens``, ``target_tokens``, ``label``. Readable records must have
    a final label from :data:`LABELS`. Explicitly unreadable records use
    ``readable=False``, ``label=None`` and zero source/target token contributions;
    their unknown real lengths are not imputed. They remain in the original
    sample for weights and variance. A sampled shard needs
    at least two records unless its entire one-row population is enumerated.
    Optional ``row_index`` values are checked for duplicate sampled rows.

    ``expected_sample_counts`` maps corpus -> shard ID -> sample count; provide
    it from the frozen sampling manifest to catch omitted rows or whole shards.
    ``source_total_tokens`` is an explicitly supplied external source-token
    total (one corpus) or corpus -> total mapping. Only when supplied is a
    source-token projection calculated. It never rescales target-token counts.
    """
    corpora = defaultdict(lambda: defaultdict(list))
    seen_indices = set()
    sample_count = 0
    for original in records:
        if not isinstance(original, Mapping):
            raise ValueError("each sample record must be a mapping")
        row = dict(original)
        for field in ("corpus", "shard_id"):
            if not isinstance(row.get(field), str) or not row[field]:
                raise ValueError(f"{field} must be a nonempty string")
        population = row.get("shard_rows")
        if isinstance(population, bool) or not isinstance(population, Integral) or population < 1:
            raise ValueError("shard_rows must be a positive integer")
        readable = row.get("readable", True)
        if not isinstance(readable, bool):
            raise ValueError("readable must be a boolean")
        row["readable"] = readable
        if readable and row.get("label") not in LABELS:
            raise ValueError("every readable sample record needs a final biology/clinical/other/mixed label")
        if not readable and ("label" not in row or row["label"] is not None):
            raise ValueError("unreadable sample records must have label=None")
        for field in ("source_tokens", "target_tokens"):
            if field not in row:
                raise ValueError(f"missing {field}")
            row[field] = _number(row[field], field)
            if not readable and row[field] != 0:
                raise ValueError("unreadable records require zero domain token contributions")
        if "row_index" in row:
            index = row["row_index"]
            if isinstance(index, bool) or not isinstance(index, Integral) or not 0 <= index < population:
                raise ValueError("row_index must lie within the shard population")
            identity = (row["corpus"], row["shard_id"], index)
            if identity in seen_indices:
                raise ValueError("duplicate sampled row_index")
            seen_indices.add(identity)
        corpora[row["corpus"]][row["shard_id"]].append(row)
        sample_count += 1
    if not sample_count:
        raise ValueError("sample must not be empty")
    observed_counts = {}
    for corpus, strata in corpora.items():
        observed_counts[corpus] = {}
        for shard_id, rows in strata.items():
            population, sample = rows[0]["shard_rows"], len(rows)
            if any(row["shard_rows"] != population for row in rows):
                raise ValueError("inconsistent shard_rows within a stratum")
            if sample > population:
                raise ValueError("sample count exceeds shard_rows")
            if sample < 2 and sample != population:
                raise ValueError("each sampled shard needs at least two independent rows")
            observed_counts[corpus][shard_id] = sample
    if expected_sample_counts is not None and observed_counts != expected_sample_counts:
        raise ValueError("sample counts do not match the frozen sampling manifest")
    if source_total_tokens is not None and any(
            not row["readable"] for strata in corpora.values() for rows in strata.values() for row in rows):
        raise ValueError("external source_total_tokens projection is invalid with unreadable sampled rows")
    if source_total_tokens is None:
        external_totals = {}
    elif isinstance(source_total_tokens, Mapping):
        if set(source_total_tokens) - set(corpora):
            raise ValueError("source_total_tokens names an unsampled corpus")
        external_totals = {name: _number(value, "source_total_tokens")
                           for name, value in source_total_tokens.items()}
    elif len(corpora) == 1:
        external_totals = {next(iter(corpora)): _number(source_total_tokens, "source_total_tokens")}
    else:
        raise ValueError("multiple corpora require a source_total_tokens mapping")
    results = {}
    for corpus, strata in sorted(corpora.items()):
        summary = {
            "sample_records": sum(map(len, strata.values())),
            "readable_sample_records": sum(row["readable"] for rows in strata.values() for row in rows),
            "unreadable_sample_records": sum(not row["readable"] for rows in strata.values() for row in rows),
            "sampled_strata": len(strata),
            "population_records": sum(rows[0]["shard_rows"] for rows in strata.values()),
            "estimate_scope": "currently readable document domain within the supplied source frame",
            "readability": _estimate(strata, lambda row: int(row["readable"]), lambda row: 1),
            "token_totals_scope": "Readable rows contribute full token counts; unreadable rows remain in the sample with zero domain contributions, not inferred actual lengths.",
            "token_totals": {unit: _estimate(strata, lambda row, unit=unit: row[unit])
                             for unit in ("source_tokens", "target_tokens")},
            "categories": {},
        }
        for category in (*LABELS, "biology_plus_mixed"):
            accepted = {"biology", "mixed"} if category == "biology_plus_mixed" else {category}
            statistics = {"documents": _estimate(strata, lambda row: int(row["label"] in accepted),
                                                  lambda row: int(row["readable"]))}
            for unit in ("source_tokens", "target_tokens"):
                statistics[unit] = _estimate(
                    strata, lambda row, unit=unit: row[unit] if row["label"] in accepted else 0,
                    lambda row, unit=unit: row[unit])
            if corpus in external_totals:
                source = statistics["source_tokens"]
                baseline = external_totals[corpus]
                statistics["source_total_projection"] = {
                    "baseline_tokens": baseline,
                    "estimate": baseline * source["share"],
                    "standard_error": baseline * source["share_standard_error"],
                    "ci95": [baseline * value for value in source["share_ci95"]],
                }
            summary["categories"][category] = statistics
        results[corpus] = summary
    return {
        "method": "stratified simple random sampling without replacement; HT totals; delta-method ratio intervals",
        "uncertainty": "Approximate 95% sampling intervals; label error, overlap and selection bias are not included.",
        "readable_domain": "Unreadable sampled rows keep original stratum weights and variance contributions; category document and token shares condition on readable content. No inference about the biology share of unreadable content is made.",
        "definition_sensitivity": "biology is the strict definition; biology_plus_mixed adds every mixed document, not an extra independent corpus.",
        "corpora": results,
    }
