# Define the targets
sender: sender.py
receiver: receiver.py

# Define the build rules
.PHONY: all
all: sender receiver

# Build sender
sender: sender.py
	@echo "Building sender..."
	# No build step needed for Python files.

# Build receiver
receiver: receiver.py
	@echo "Building receiver..."
	# No build step needed for Python files.

# Define targets for running sender and receiver
.PHONY: run-sender
run-sender: sender
	python sender.py

.PHONY: run-receiver
run-receiver: receiver
	python receiver.py

# Clean the generated files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	# No clean-up needed for Python files.

