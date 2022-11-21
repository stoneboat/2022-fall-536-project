export PORT ?= 11111

SCRIPTS = scripts

SRCS_DIR = ./srcs
SCS = $(SRCS_DIR)/server # Student C server
SCC = $(SRCS_DIR)/client # Student C client
SPC = $(SRCS_DIR)/client-3wh.py # Student 3WH python client

WORKSPACE_DIR = .workspace
NUM_CORRECT = 0

MAKEFLAGS += --no-print-directory

export nhost ?= 2

.PHONY: tests-c tests-python all-tests

# Usage: make -f Congestion_Tests.mak tests-c nhost=2
tests-c: 
	@#	Generate a long random input
	@mkdir -p $(WORKSPACE_DIR)
	@head -c100 /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' > $(WORKSPACE_DIR)/test_message.txt

	@#	Start the server
	@mkdir -p $(WORKSPACE_DIR)
	@$(SCRIPTS)/utils/mn-stratum/exec-d-script h1 \
		"$(SCS) $(PORT) > $(WORKSPACE_DIR)/test_output.text"
	@sleep 0.2

	@#	Let the client send message to server
	@for hostId in `seq 2 $(nhost)`; \
	do \
		$(SCRIPTS)/utils/mn-stratum/exec-script h$$hostId \
		"$(SCC) 10.0.0.1 $(PORT) < $(WORKSPACE_DIR)/test_message.txt > /dev/null"; \
		sleep 0.1; \
	done

	@#	Stop the server
	@$(SCRIPTS)/utils/mn-stratum/exec-d-script h1 \
		"pkill -f $(SCS)"
	@sleep 0.2


# Usage: make -f Congestion_Tests.mak tests-python nhost=2	
tests-python: 
	@echo $(nhost)
	@echo Have not implemented yet

	
all-tests: tests-c tests-python