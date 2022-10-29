.DEFAULT_GOAL := help


### QUICK
# ¯¯¯¯¯¯¯

install: server.install worker.install ## Install

daemon: worker.daemon server.daemon## Start daemon

stop: server.stop


include makefiles/server.mk
include makefiles/test.mk
include makefiles/database.mk
include makefiles/format.mk
include makefiles/help.mk
include makefiles/worker.mk
