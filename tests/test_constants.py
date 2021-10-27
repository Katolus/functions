from functions.constants import CloudServiceType


def test_cloud_service_type():
    assert CloudServiceType.CLOUD_FUNCTION == "cloud_function"

    assert CloudServiceType.all() == ["cloud_function"]
