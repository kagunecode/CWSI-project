# CWSI-project
Project related to the CWSI calculation

# UPDATES
Using Olympe 7.5.0 since Oylmpe 7.7.0 causes constant connection retries. This has been fixed on the current version of this program. Requirements have been updated to use the functional Olympe version.
Multiprocessing is being used as of now in this program since matplotlib blocks the program from executing any following code. For now, it's the best solution as it has no impact on the performance of the live stream video at all.
Also, the venv used needs a cleanup since there are a lot of packages that are not being used at all.
