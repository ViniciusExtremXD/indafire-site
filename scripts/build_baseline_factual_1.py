"""Rebuild the private BASELINE-FACTUAL-1 runtime from immutable sources."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ROOT = ROOT / "audit" / "private" / "task-2"

TABLE_PREFIX = "wp_indafire_2021_"
SOURCE_DATABASE = "BASELINE_RAW_SOURCE"
TARGET_DATABASE = "BASELINE_FACTUAL_1"
VERIFY_DATABASE = "BASELINE_FACTUAL_1_FINAL_VERIFY"
SOURCE_VERIFY_DATABASE = "BASELINE_FACTUAL_1_SOURCE_VERIFY"

DYNAMIC_OPTION_NAMES = (
    "elementor_log",
    "elementor_pro_license_key",
    "_elementor_pro_license_data",
    "fs_active_plugins",
    "WooLentorPro_lic_email",
)

class BaselineBuildError(RuntimeError):
    """Raised when baseline build operations fail."""


def build_dynamic_database_normalization_sql(target_database: str, canonical_database: str) -> str:
    if target_database != TARGET_DATABASE or canonical_database != VERIFY_DATABASE:
        raise BaselineBuildError("Dynamic normalization identities are not fixed")
    option_names = ", ".join(f"'{name}'" for name in DYNAMIC_OPTION_NAMES)
    return (
        f"UPDATE `{TARGET_DATABASE}`.`{TABLE_PREFIX}options` AS target "
        f"INNER JOIN `{VERIFY_DATABASE}`.`{TABLE_PREFIX}options` AS canonical "
        f"ON canonical.option_id=target.option_id AND canonical.option_name=target.option_name "
        f"SET target.option_value=canonical.option_value, target.autoload=canonical.autoload "
        f"WHERE target.option_name IN ({option_names});"
    )
