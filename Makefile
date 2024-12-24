# Define variables
PYTHON=python3.11

# Default target
all: build

# Target to build the application
build: install-deps
	@echo "Building the application..."
	$(PYTHON) -m PyInstaller --onefile main.py
	@echo "Build completed!"

# Target to install dependencies
install-deps: install-pkg-pip install-pip-pyinstaller
	@echo "Dependencies installation completed!"

# Install pip using pkg
install-pkg-pip:
	@echo "Installing pip using pkg..."
	sudo pkg ins py311-pip

# Install pyinstaller using pip
install-pip-pyinstaller:
	@echo "Installing PyInstaller using pip..."
	sudo $(PYTHON) -m pip install pyinstaller

# Target to clean up build artifacts
clean:
	@echo "Cleaning up..."
	rm -rf dist build *.spec
	@echo "Clean up completed!"

# Target to install the binary
install:
	@echo "Installing the application..."
	sudo cp dist/main /usr/local/bin/prs
	@echo "Installation completed!"

# Target to uninstall the binary
uninstall:
	@echo "Uninstalling the application..."
	sudo rm -f /usr/local/bin/prs
	@echo "Uninstallation completed!"

