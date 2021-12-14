from django.dispatch import Signal


transaction_complete_signal = Signal(providing_args=["instance"])
