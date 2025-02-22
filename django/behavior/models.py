
from django.db import models
from common.models import Log

# Create your models here.
class BehaviorOption(models.Model):
    # we need to keep the reference to the log here because the xabsl code could change between logs,
    # changing the options and the states in it as well
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_options')
    # this id depends on the order it appears in the BehaviorStateComplete representation
    # we need this to get the actual option id during insertion of BehaviorStateSparse
    # lookup looks like this: client.list(log_id=log_id, xabsl_internal_id=<id in BehaviorStateSparse>)
    xabsl_internal_option_id = models.IntegerField(blank=True, null=True)
    option_name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.option_name}"


class BehaviorOptionState(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_options_states')
    option_id = models.ForeignKey(BehaviorOption, on_delete=models.CASCADE, related_name='behavior_options_states')
    # state id within an option - this is the id BehaviorFrameOption.activeState refers to
    xabsl_internal_state_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    target = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.name}"


class BehaviorFrameOption(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_frame_option')
    options_id = models.ForeignKey(BehaviorOption,on_delete=models.CASCADE, related_name='behavior_frame_option')
    active_state = models.ForeignKey(BehaviorOptionState,on_delete=models.CASCADE, related_name='behavior_frame_option')

    # parent can't be a foreign key for now because we identify the root option with -1. 
    # TODO add root option with id -1 => would mean we manually need to create the id column and handle the primary key behavior
    #parent = models.ForeignKey(BehaviorOption,to_field='id', on_delete=models.CASCADE, related_name='behavior_frame_options_parent')
    #parent = models.IntegerField(blank=True, null=True)
    frame = models.IntegerField(blank=True, null=True)
    #time = models.IntegerField(blank=True, null=True)
    #time_of_execution = models.IntegerField(blank=True, null=True)
    #state_time = models.IntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame', 'options_id']),
        ]
        unique_together = ('log_id', 'options_id', 'frame', 'active_state')


class XabslSymbolComplete(models.Model):
    log_id = models.OneToOneField(Log,on_delete=models.CASCADE, related_name='xabsl_symbol_complete', primary_key=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id']),
        ]
        verbose_name_plural = "XabslSymbolComplete"

class XabslSymbolSparse(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='xabsl_symbol_sparse')
    frame = models.IntegerField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame']),
        ]
        unique_together = ('log_id', 'frame')
        verbose_name_plural = "XabslSymbolSparse"
