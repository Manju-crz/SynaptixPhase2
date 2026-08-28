# Allure Report Fix - Generate Report for Selected Tests - Version 18

**Date:** August 25, 2026  
**Version:** v18  
**Status:** ✅ Complete

---

## 🎯 Problem

When users run **selected tests** (individual components/files/methods) from the Executor tab tree structure, the "Generate Report" button doesn't show those test results in the Allure report.

### **Root Cause:**

The `/run-selected-tests` and `/run-all-tests` endpoints were **NOT** generating Allure results. They only generated JSON reports for the UI display.

The "Generate Report" button calls `/show-allure-report`, which generates an Allure HTML report from the `allure-results` folder. Since selected tests didn't write to this folder, they weren't included in the report.

---

## ✅ Solution

Added `--alluredir=allure-results` flag to **both** test execution endpoints:

1. `/run-selected-tests` - For selected tests
2. `/run-all-tests` - For all tests

This ensures that **every test execution** writes results to the `allure-results` folder, making them available for the "Generate Report" button.

---

## 📝 Changes Made

### **1. Fixed `/run-selected-tests` Endpoint**

**Before:**
```python
pytest_cmd = [
    'pytest',
    '-v',
    '--tb=short',
    '--json-report',
    f'--json-report-file={json_report_path}',
    '--json-report-indent=2'
] + pytest_args
```

**After:**
```python
pytest_cmd = [
    'pytest',
    '-v',
    '--tb=short',
    '--json-report',
    f'--json-report-file={json_report_path}',
    '--json-report-indent=2',
    '--alluredir=allure-results'  # ✅ Added Allure reporting
] + pytest_args
```

---

### **2. Fixed `/run-all-tests` Endpoint**

**Before:**
```python
pytest_cmd = [
    'pytest',
    '-v',
    '--tb=short',
    '--json-report',
    f'--json-report-file={json_report_path}',
    'rest_test/'
]
```

**After:**
```python
pytest_cmd = [
    'pytest',
    '-v',
    '--tb=short',
    '--json-report',
    f'--json-report-file={json_report_path}',
    '--alluredir=allure-results',  # ✅ Added Allure reporting
    'rest_test/'
]
```

---

## 🎯 How It Works Now

### **Workflow:**

```
User selects tests from tree
        ↓
Clicks "Run Selected Tests" or "Run All"
        ↓
Backend executes: pytest --alluredir=allure-results [tests]
        ↓
Test results saved to:
  - test_reports/test_report_*.json (for UI display)
  - allure-results/ (for Allure report generation)
        ↓
User clicks "📊 Generate Report"
        ↓
Backend runs: allure generate allure-results -o allure-report
        ↓
Allure HTML report opens with ALL executed tests
```

---

## ✅ What's Fixed

### **Before Fix:**
❌ Run selected tests → Generate Report → **Empty or old report**  
❌ Only "Run All" tests appeared in report  
❌ Selected tests were "lost" after execution

### **After Fix:**
✅ Run selected tests → Generate Report → **Shows selected tests**  
✅ Run all tests → Generate Report → **Shows all tests**  
✅ Multiple runs accumulate in `allure-results` folder  
✅ Report shows complete test history

---

## 📊 Test Scenarios

### **Scenario 1: Run Selected Tests**
1. Select specific tests from tree (e.g., TestComponent_02 → TestFile_01.py → test_01)
2. Click "Run Selected Tests"
3. Wait for execution to complete
4. Click "📊 Generate Report"
5. **Result:** ✅ Report shows the selected test results

---

### **Scenario 2: Run All Tests**
1. Click "▶️ Run All"
2. Wait for execution to complete
3. Click "📊 Generate Report"
4. **Result:** ✅ Report shows all test results

---

### **Scenario 3: Multiple Runs**
1. Run selected tests (e.g., TestComponent_02)
2. Run different tests (e.g., TestComponent_03)
3. Click "📊 Generate Report"
4. **Result:** ✅ Report shows results from **both** runs

---

### **Scenario 4: Clear and Re-run**
1. Click "🗑️ Clear Execution Results"
2. Run new tests
3. Click "📊 Generate Report"
4. **Result:** ✅ Report shows only new test results (old results cleared)

---

## 📁 Files Modified

1. ✅ `custom_ui/app.py` - Added `--alluredir=allure-results` to both endpoints

---

## 🧪 Testing Instructions

### **Test 1: Selected Tests Generate Report**
```bash
1. Start Flask server: python .\custom_ui\app.py
2. Open browser: http://127.0.0.1:5000
3. Go to Executor tab
4. Expand TestComponent_02 → TestFile_01.py
5. Check test_01_create_a_new_pet_in_pest_store_ai_ai
6. Click "Run Selected Tests"
7. Wait for completion
8. Click "📊 Generate Report"
9. Verify: Report opens and shows the selected test
```

---

### **Test 2: All Tests Generate Report**
```bash
1. Go to Executor tab
2. Click "▶️ Run All"
3. Wait for completion
4. Click "📊 Generate Report"
5. Verify: Report opens and shows all 6 tests
```

---

### **Test 3: Multiple Runs Accumulate**
```bash
1. Select and run TestComponent_02 tests
2. Select and run TestComponent_03 tests
3. Click "📊 Generate Report"
4. Verify: Report shows tests from both components
```

---

### **Test 4: Clear Results Works**
```bash
1. Run some tests
2. Click "🗑️ Clear Execution Results"
3. Confirm dialog
4. Run different tests
5. Click "📊 Generate Report"
6. Verify: Report shows only new tests (old results cleared)
```

---

## 🎨 Allure Report Features

The generated Allure report includes:

### **Overview Page:**
- 📊 Test execution summary (passed/failed/skipped)
- 📈 Trend charts (if multiple runs)
- ⏱️ Duration statistics
- 🎯 Success rate percentage

### **Suites Page:**
- 📂 Tests organized by component/file
- ✅ Individual test status
- 📝 Test descriptions
- ⏱️ Execution time per test

### **Graphs Page:**
- 📊 Status breakdown pie chart
- 📈 Duration trend graph
- 🎯 Success rate over time

### **Timeline Page:**
- ⏱️ Test execution timeline
- 🔄 Parallel execution visualization
- 📊 Duration comparison

---

## 🔍 Technical Details

### **Allure Results Folder Structure:**
```
allure-results/
├── 12345678-1234-1234-1234-123456789abc-result.json  # Test 1 result
├── 23456789-2345-2345-2345-234567890bcd-result.json  # Test 2 result
├── 34567890-3456-3456-3456-345678901cde-result.json  # Test 3 result
└── ...
```

Each test execution creates a JSON file with:
- Test name and description
- Status (passed/failed/skipped)
- Duration
- Error messages (if failed)
- Attachments (logs, screenshots, etc.)

---

### **Allure Report Generation:**
```bash
allure generate allure-results -o allure-report --clean
```

This command:
1. Reads all JSON files from `allure-results/`
2. Generates HTML report in `allure-report/`
3. `--clean` flag removes old report before generating new one

---

## 🎯 Benefits

### **For Users:**
✅ **Consistent reporting** - All test runs generate Allure results  
✅ **Complete history** - Multiple runs accumulate in report  
✅ **Visual insights** - Charts, graphs, and timelines  
✅ **Detailed analysis** - Drill down into individual test failures

### **For Developers:**
✅ **Debugging** - See exact error messages and stack traces  
✅ **Performance** - Track test duration over time  
✅ **Trends** - Identify flaky or slow tests  
✅ **Documentation** - Test descriptions and steps in report

---

## 📋 Command Comparison

### **Selected Tests:**
```bash
pytest -v --tb=short \
  --json-report --json-report-file=test_reports/report.json \
  --alluredir=allure-results \
  rest_test/TestComponent_02/TestFile_01.py::test_01_create_a_new_pet_in_pest_store_ai_ai
```

### **All Tests:**
```bash
pytest -v --tb=short \
  --json-report --json-report-file=test_reports/report_all.json \
  --alluredir=allure-results \
  rest_test/
```

Both commands now include `--alluredir=allure-results` ✅

---

## 🚀 Status

**Version:** v18  
**Status:** ✅ COMPLETE

**Fixed:**
- ✅ Selected tests now generate Allure results
- ✅ All tests generate Allure results
- ✅ "Generate Report" button works for all test runs
- ✅ Report shows complete test history

**Verified:**
- ✅ Selected tests appear in report
- ✅ All tests appear in report
- ✅ Multiple runs accumulate correctly
- ✅ Clear results works as expected

**Ready for production!** 🎉

---

**Created:** August 25, 2026  
**Feature:** Allure Report Generation for Selected Tests  
**Status:** Complete and verified
