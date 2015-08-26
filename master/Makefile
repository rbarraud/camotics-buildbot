# -*- makefile -*-

# This is a simple makefile which lives in a buildmaster/buildslave
# directory (next to the buildbot.tac file). It allows you to start/stop the
# master or slave by doing 'make start' or 'make stop'.

# The 'reconfig' target will tell a buildmaster to reload its config file.

start:
	twistd --no_save -y buildbot.tac

stop:
	wc -l twistd.log | sed 's/^\([0-9]*\).*$$/\1/' >line.txt
	-PID=$$(cat twistd.pid); kill $$PID
	while ! tail -n +$(shell cat line.txt) twistd.log |\
      grep "Server Shut Down." >/dev/null; do sleep 1; done

reconfig:
	kill -HUP `cat twistd.pid`

restart:
	$(MAKE) stop
	git pull
	$(MAKE) start

log:
	tail -f twistd.log
