export PORT ?= 11111

SCRIPTS = scripts

SRCS_DIR = ./srcs
SCS = $(SRCS_DIR)/server # Student C server
SCC = $(SRCS_DIR)/client # Student C client
SPC = $(SRCS_DIR)/client-3wh.py # Student 3WH python client

WORKSPACE_DIR = .workspace
NUM_CORRECT = 0

MAKEFLAGS += --no-print-directory

.PHONY: tests tests-3wh all-tests


tests: 
	@echo Haven not implemented yet
	
tests-3wh: 
	@echo Haven not implemented yet
	
all-tests: tests tests-3wh