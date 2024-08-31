from .base_client import VaapiBase, AsyncVaapiBase
#from .tasks.client_ext import TasksClientExt, AsyncTasksClientExt
#from .projects.client_ext import ProjectsClientExt, AsyncProjectsClientExt


class Vaapi(VaapiBase):
    """"""
    __doc__ += VaapiBase.__doc__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.tasks = TasksClientExt(client_wrapper=self._client_wrapper)
        #self.projects = ProjectsClientExt(client_wrapper=self._client_wrapper)


class AsyncVaapi(AsyncVaapiBase):
    """"""
    __doc__ += AsyncVaapiBase.__doc__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.tasks = AsyncTasksClientExt(client_wrapper=self._client_wrapper)
        #self.projects = AsyncProjectsClientExt(client_wrapper=self._client_wrapper)