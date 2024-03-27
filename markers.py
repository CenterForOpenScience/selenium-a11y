import pytest

import settings

smoke_test = pytest.mark.smoke_test
core_functionality = pytest.mark.core_functionality
dont_run_on_prod = pytest.mark.skipif(
    settings.PRODUCTION, reason="Test should not run on production"
)
dont_run_on_preferred_node = pytest.mark.skipif(
    bool(settings.PREFERRED_NODE),
    reason="Test makes breaking changes to preferred node",
)

ember_page = pytest.mark.ember_page
legacy_page = pytest.mark.legacy_page
