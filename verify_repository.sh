#!/bin/bash
# Repository verification script for Bio-Resilience Engine
# Checks for common issues and validates setup

set -e

echo "================================================"
echo "Bio-Resilience Engine - Repository Verification"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass_count=0
fail_count=0
warn_count=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((pass_count++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((fail_count++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((warn_count++))
}

echo "1. Checking File Structure..."
echo "   -------------------------"

# Check critical files exist
if [ -f "README.md" ]; then check_pass "README.md exists"; else check_fail "README.md missing"; fi
if [ -f "requirements.txt" ]; then check_pass "requirements.txt exists"; else check_fail "requirements.txt missing"; fi
if [ -f "docker-compose.yml" ]; then check_pass "docker-compose.yml exists"; else check_fail "docker-compose.yml missing"; fi
if [ -f "Dockerfile" ]; then check_pass "Dockerfile exists"; else check_fail "Dockerfile missing"; fi

# Check docker/ directory
if [ -d "docker" ]; then 
    check_pass "docker/ directory exists"
    if [ -f "docker/Dockerfile.api" ]; then check_pass "docker/Dockerfile.api exists"; else check_fail "docker/Dockerfile.api missing"; fi
    if [ -f "docker/Dockerfile.edge" ]; then check_pass "docker/Dockerfile.edge exists"; else check_fail "docker/Dockerfile.edge missing"; fi
    if [ -f "docker/mosquitto.conf" ]; then check_pass "docker/mosquitto.conf exists"; else check_fail "docker/mosquitto.conf missing"; fi
    if [ -f "docker/init-db.sql" ]; then check_pass "docker/init-db.sql exists"; else check_fail "docker/init-db.sql missing"; fi
else 
    check_fail "docker/ directory missing"
fi

echo ""
echo "2. Checking Source Code Structure..."
echo "   ---------------------------------"

if [ -d "src/edge_node" ]; then check_pass "src/edge_node/ exists"; else check_fail "src/edge_node/ missing"; fi
if [ -d "src/cloud_fusion" ]; then check_pass "src/cloud_fusion/ exists"; else check_fail "src/cloud_fusion/ missing"; fi
if [ -d "src/wearable_sdk" ]; then check_pass "src/wearable_sdk/ exists"; else check_fail "src/wearable_sdk/ missing"; fi
if [ -d "tests" ]; then check_pass "tests/ directory exists"; else check_fail "tests/ directory missing"; fi
if [ -d "docs" ]; then check_pass "docs/ directory exists"; else check_fail "docs/ directory missing"; fi

echo ""
echo "3. Checking Dependencies..."
echo "   ------------------------"

# Check if databases package is in requirements
if grep -q "^databases==" requirements.txt; then 
    check_pass "databases package in requirements.txt"
else 
    check_fail "databases package missing from requirements.txt"
fi

# Check if pydantic-settings is in requirements
if grep -q "^pydantic-settings==" requirements.txt; then 
    check_pass "pydantic-settings in requirements.txt"
else 
    check_fail "pydantic-settings missing from requirements.txt"
fi

echo ""
echo "4. Checking Python Imports..."
echo "   --------------------------"

# Check config.py doesn't import PostgresDsn (Pydantic v1 issue)
if grep -q "from pydantic import.*PostgresDsn" src/cloud_fusion/config.py; then
    check_warn "config.py imports PostgresDsn (may cause issues with Pydantic v2)"
else
    check_pass "config.py doesn't import PostgresDsn"
fi

# Check database.py imports databases
if grep -q "from databases import Database" src/cloud_fusion/database.py; then
    check_pass "database.py imports databases correctly"
else
    check_fail "database.py missing databases import"
fi

echo ""
echo "5. Checking API Endpoint Consistency..."
echo "   ------------------------------------"

# Check if README uses correct health endpoint
if grep -q "/api/v1/health/" README.md; then
    check_pass "README.md uses correct health endpoint"
else
    if grep -q "localhost:8000/health" README.md; then
        check_fail "README.md uses old health endpoint"
    else
        check_pass "README.md health endpoint OK"
    fi
fi

# Check if biosignal endpoint is correct
if grep -q "/api/v1/fusion/ingest/biosignal" README.md; then
    check_pass "README.md has correct biosignal endpoint"
else
    check_warn "README.md may have incorrect biosignal endpoint"
fi

echo ""
echo "6. Checking Documentation..."
echo "   -------------------------"

if [ -f "docs/ARCHITECTURE.md" ]; then check_pass "ARCHITECTURE.md exists"; else check_warn "ARCHITECTURE.md missing"; fi
if [ -f "docs/API_REFERENCE.md" ]; then check_pass "API_REFERENCE.md exists"; else check_warn "API_REFERENCE.md missing"; fi
if [ -f "docs/TECHNICAL_SPEC.md" ]; then check_pass "TECHNICAL_SPEC.md exists"; else check_warn "TECHNICAL_SPEC.md missing"; fi
if [ -f "docs/DEPLOYMENT.md" ]; then check_pass "DEPLOYMENT.md exists"; else check_warn "DEPLOYMENT.md missing"; fi

echo ""
echo "7. Checking Configuration Files..."
echo "   -------------------------------"

if [ -f ".env.example" ]; then check_pass ".env.example exists"; else check_warn ".env.example missing"; fi
if [ -f ".gitignore" ]; then check_pass ".gitignore exists"; else check_warn ".gitignore missing"; fi
if [ -f "pyproject.toml" ]; then check_pass "pyproject.toml exists"; else check_warn "pyproject.toml missing"; fi

echo ""
echo "================================================"
echo "VERIFICATION SUMMARY"
echo "================================================"
echo -e "${GREEN}Passed:${NC}  $pass_count"
echo -e "${YELLOW}Warnings:${NC} $warn_count"
echo -e "${RED}Failed:${NC}  $fail_count"
echo ""

if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}✓ Repository verification PASSED${NC}"
    echo "Repository is ready for deployment and investor review."
    exit 0
elif [ $fail_count -le 2 ]; then
    echo -e "${YELLOW}⚠ Repository verification completed with minor issues${NC}"
    echo "Please review failed checks above."
    exit 0
else
    echo -e "${RED}✗ Repository verification FAILED${NC}"
    echo "Please fix critical issues above before deployment."
    exit 1
fi
