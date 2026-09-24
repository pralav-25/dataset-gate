"""Discover the exact rule catalog supported by this running version."""

from fastapi import APIRouter

from dataset_gate.catalog import rule_catalog

router = APIRouter(tags=["Contracts"])


@router.get("/rules")
def rules():
    return rule_catalog()
