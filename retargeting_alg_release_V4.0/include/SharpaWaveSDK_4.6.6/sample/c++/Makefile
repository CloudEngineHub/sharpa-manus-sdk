# Makefile for Sharpa sample programs
# This Makefile intelligently detects library and include paths

CXX = g++
CXXFLAGS = -std=c++17 -g -O0 -Wall -Wextra -DDEBUG -D_DEBUG
BUILD_DIR = build/

# Function to check if a path exists and contains required files
$(info $(shell ls -l ../../lib))
ifeq ($(UNAME_S),Darwin)
    CHECK_RELEASE = $(shell if [ -f "../../lib/libSharpaWaveSDKWrapper.dylib" ]; then echo "local"; fi)
    CHECK_BUILD = $(shell if [ -d "../../build/install/lib" ]; then echo "build"; fi)
else
    CHECK_RELEASE = $(shell if [ -f "../../lib/libSharpaWaveSDKWrapper.so" ]; then echo "local"; fi)
    CHECK_BUILD = $(shell if [ -d "../../build/install/lib" ]; then echo "build"; fi)
endif
$(info $(CHECK_RELEASE))
$(info $(CHECK_DIST))
$(info $(CHECK_BUILD))
# Determine paths based on what exists
ifeq ($(CHECK_BUILD),build)
    INCLUDE_DIR = ../../build/install/include
    LIB_DIR = ../../build/install/lib
    LIBS = -lSharpaWaveSDK -lSharpaHand -ltactile_sdk -lspdlog -lfmt -lyaml-cpp -lmsgpack11
    $(info Using ../../build/install as root directory)
else ifeq ($(CHECK_RELEASE),local)
    INCLUDE_DIR = ../../include
    LIB_DIR = ../../lib
    LIBS = -lSharpaWaveSDKWrapper -ldl
    $(info Using local lib/ and include/ directories)
else
    $(error Error: Could not find Sharpa libraries and headers. Please ensure: 1. SharpaRT is installed in release folder OR 2. ../../build/install directory exists with lib/ and include/)
endif

# Convert relative paths to absolute paths
ABS_INCLUDE_DIR = $(shell realpath $(INCLUDE_DIR))
ABS_LIB_DIR = $(shell realpath $(LIB_DIR))

# Display configuration
$(info Build Configuration:)
$(info   Include Directory: $(INCLUDE_DIR) -> $(ABS_INCLUDE_DIR))
$(info   Library Directory: $(LIB_DIR) -> $(ABS_LIB_DIR))

TARGET = $(BUILD_DIR)/sharpa_tactile_example
SOURCE = sharpa_tactile_example.cc
TARGET2 = $(BUILD_DIR)/sharpa_wave_example
SOURCE2 = sharpa_wave_example.cc

# Linker flags with RPATH to remember absolute library path
LDFLAGS = -Wl,--allow-multiple-definition -static-libgcc -static-libstdc++ -rdynamic -Wl,-rpath,$(ABS_LIB_DIR)

# Default target - build all examples
all: $(BUILD_DIR) $(TARGET) $(TARGET2) $(TARGET3)

# Create build directory
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Build sharpa_tactile_example
$(TARGET): $(SOURCE) | $(BUILD_DIR)
	@echo "Building sharpa_tactile_example..."
	@echo "  Using absolute library path: $(ABS_LIB_DIR)"
	$(CXX) $(CXXFLAGS) $(SOURCE) \
		-L$(ABS_LIB_DIR) $(LIBS) \
		-I$(ABS_INCLUDE_DIR) \
		$(LDFLAGS) \
		-o $(TARGET)
	@echo "✓ sharpa_tactile_example built successfully"
	@echo "  RPATH set to: $(ABS_LIB_DIR)"

# Build sharpa_wave_example
$(TARGET2): $(SOURCE2) | $(BUILD_DIR)
	@echo "Building sharpa_wave_example..."
	@echo "  Using absolute library path: $(ABS_LIB_DIR)"
	$(CXX) $(CXXFLAGS) $(SOURCE2) \
		-L$(ABS_LIB_DIR) $(LIBS) \
		-I$(ABS_INCLUDE_DIR) \
		$(LDFLAGS) \
		-o $(TARGET2)
	@echo "✓ sharpa_wave_example built successfully"
	@echo "  RPATH set to: $(ABS_LIB_DIR)"

# Build only tactile example
tactile: $(BUILD_DIR) $(TARGET)

# Build only wave example
wave: $(BUILD_DIR) $(TARGET2)

# Clean target
clean:
	@echo "Cleaning build directory..."
	@rm -f $(TARGET) $(TARGET2) $(TARGET3)
	@rm -rf $(BUILD_DIR)
	@echo "✓ Clean complete"

# Help target
help:
	@echo "Sharpa Sample Makefile"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all      Build all sample programs (default)"
	@echo "  tactile  Build only sharpa_tactile_example"
	@echo "  wave     Build only sharpa_wave_example"
	@echo "  clean    Clean build directory"
	@echo "  help     Show this help message"
	@echo ""
	@echo "This Makefile automatically detects library and include paths:"
	@echo "  1. Checks for system-wide installation (/usr/include/sharpa and /usr/lib/sharpa-wave-sdk)"
	@echo "  2. Falls back to ../../build/install"
	@echo ""
	@echo "Current configuration:"
	@echo "  Include Directory: $(INCLUDE_DIR) -> $(ABS_INCLUDE_DIR)"
	@echo "  Library Directory: $(LIB_DIR) -> $(ABS_LIB_DIR)"
	@echo ""
	@echo "Note: Targets are built with RPATH to remember absolute library paths"

.PHONY: all tactile wave clean help
