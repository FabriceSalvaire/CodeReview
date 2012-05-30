####################################################################################################
#
# How to start
#
####################################################################################################

# Set environment
. setenv.sh 

# Cleanup the repository
./tools/clean 

# Build
python setup.py build

# Update TAGS file
./tools/update-tags 

# Check licence
./tools/check-license.sh 

# Generate RST files
./tools/generate-rst 
# Generate HTML Documentation
cd sphinx/
./make-html --clean

####################################################################################################
#
# End
#
####################################################################################################
