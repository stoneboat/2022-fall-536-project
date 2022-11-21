export PORT ?= 11111

SCRIPTS_DIR = scripts

SRCS_DIR = ./srcs
SCS = $(SRCS_DIR)/server # Student C server
SCC = $(SRCS_DIR)/client # Student C client
SPC = $(SRCS_DIR)/client-3wh.py # Student 3WH python client

WORKSPACE_DIR = .workspace
NUM_CORRECT = 0

MAKEFLAGS += --no-print-directory

export nhost ?= 2
export nbits ?= 2

.PHONY: tests-c tests-python all-tests

# Usage: make -f Congestion_Tests.mak tests-c nhost=2 nbits=100
tests-c: 
	@$(SCRIPTS_DIR)/project/parallel-client-c-sh $(nhost) $(nbits)


# Usage: make -f Congestion_Tests.mak tests-python nhost=2	
tests-python: 
	@echo Have not implemented yet

	
all-tests: tests-c tests-python