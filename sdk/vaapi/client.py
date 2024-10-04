from .base_client import VaapiBase, AsyncVaapiBase


class Vaapi(VaapiBase):
    """"""
    __doc__ += VaapiBase.__doc__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AsyncVaapi(AsyncVaapiBase):
    """"""
    __doc__ += AsyncVaapiBase.__doc__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
