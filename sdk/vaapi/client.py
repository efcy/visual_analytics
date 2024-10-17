from .base_client import VaapiBase


class Vaapi(VaapiBase):
    """"""
    __doc__ += VaapiBase.__doc__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
