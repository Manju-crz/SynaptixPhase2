# Migration Test Plan - Configuration Tab

## 🎯 Test Objective

Verify that the Configuration tab migration maintains 100% functionality and backward compatibility.

---

## ✅ Pre-Test Checklist

- [ ] Server is stopped
- [ ] Browser cache cleared
- [ ] Browser console open (F12)
- [ ] Network tab open (to check for 404s)

---

## 🧪 Test Cases

### Test 1: Page Load

**Steps:**
1. Start server: `python custom_ui/app.py`
2. Open browser to `http://localhost:5000`
3. Check browser console for errors

**Expected:**
- ✅ Page loads without errors
- ✅ Configuration tab is active by default
- ✅ No 404 errors in Network tab
- ✅ No JavaScript errors in Console

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 2: Configuration Tab Display

**Steps:**
1. Look at Configuration tab content
2. Verify all sections are visible

**Expected:**
- ✅ "⚙️ Configuration" header visible
- ✅ "🤖 AI Model Configuration" section visible
- ✅ AI Model dropdown visible with 3 options
- ✅ Model information box visible
- ✅ API Keys warning box visible
- ✅ "🔧 System Information" section visible
- ✅ All info items displayed
- ✅ "Current AI Model" shows a value

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 3: AI Model Selection (Old Function)

**Steps:**
1. Open browser console
2. Type: `saveAiModelConfig()`
3. Press Enter

**Expected:**
- ✅ Function executes without error
- ✅ Success message appears (green box)
- ✅ Console shows: "AI Model configuration saved: [model]"
- ✅ No errors in console

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 4: AI Model Selection (UI Interaction)

**Steps:**
1. Select "DeepSeek - v4-coder" from dropdown
2. Wait 3 seconds
3. Check "Current AI Model" in System Information

**Expected:**
- ✅ Green success message appears
- ✅ Toast notification appears (top-right) ✨ NEW
- ✅ "Current AI Model" updates to "DeepSeek v4-coder"
- ✅ Success message disappears after 3 seconds
- ✅ Toast notification disappears after 3 seconds

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 5: AI Model Selection (Different Models)

**Steps:**
1. Select "OpenAI - GPT-4o-mini"
2. Wait for confirmation
3. Select "Groq - Llama-3.3-70b-versatile"
4. Wait for confirmation

**Expected:**
- ✅ Each selection shows success message
- ✅ Each selection shows toast notification ✨ NEW
- ✅ "Current AI Model" updates each time
- ✅ No errors in console

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 6: LocalStorage Persistence

**Steps:**
1. Select "DeepSeek - v4-coder"
2. Wait for confirmation
3. Open browser console
4. Type: `localStorage.getItem('synaptix_ai_model')`
5. Press Enter

**Expected:**
- ✅ Returns: "deepseek"
- ✅ No errors

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 7: Page Reload Persistence

**Steps:**
1. Select "Groq - Llama-3.3-70b-versatile"
2. Wait for confirmation
3. Refresh page (F5)
4. Check dropdown value
5. Check "Current AI Model"

**Expected:**
- ✅ Dropdown shows "Groq - Llama-3.3-70b-versatile"
- ✅ "Current AI Model" shows "Groq Llama-3.3-70b"
- ✅ No errors on reload

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 8: New ConfigurationPage Class

**Steps:**
1. Open browser console
2. Type: `configurationPage`
3. Press Enter
4. Type: `configurationPage.getSelectedModel()`
5. Press Enter

**Expected:**
- ✅ First command shows ConfigurationPage object
- ✅ Second command returns current model (e.g., "groq")
- ✅ No errors

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 9: Notification Component

**Steps:**
1. Open browser console
2. Type: `notification.success('Test success!')`
3. Type: `notification.error('Test error!')`
4. Type: `notification.warning('Test warning!')`
5. Type: `notification.info('Test info!')`

**Expected:**
- ✅ Each notification appears in top-right
- ✅ Each has correct color/icon
- ✅ Each auto-dismisses after timeout
- ✅ Multiple notifications stack vertically
- ✅ Close button (×) works

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 10: Storage Utility

**Steps:**
1. Open browser console
2. Type: `Storage.save('test', {foo: 'bar'})`
3. Type: `Storage.load('test')`
4. Type: `Storage.remove('test')`
5. Type: `Storage.load('test', 'default')`

**Expected:**
- ✅ First command returns true
- ✅ Second command returns {foo: 'bar'}
- ✅ Third command returns true
- ✅ Fourth command returns 'default'
- ✅ No errors

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 11: Validators Utility

**Steps:**
1. Open browser console
2. Type: `Validators.isUrl('https://example.com')`
3. Type: `Validators.isUrl('not a url')`
4. Type: `Validators.isExcelFile('test.xlsx')`
5. Type: `Validators.isExcelFile('test.txt')`

**Expected:**
- ✅ First command returns true
- ✅ Second command returns false
- ✅ Third command returns true
- ✅ Fourth command returns false
- ✅ No errors

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 12: Tab Switching

**Steps:**
1. Click "✨ Features" tab
2. Click "⚙️ Configuration" tab
3. Check if Configuration tab still works

**Expected:**
- ✅ Tabs switch correctly
- ✅ Configuration tab content still visible
- ✅ Dropdown still works
- ✅ No errors when switching back

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 13: Backward Compatibility - Legacy Functions

**Steps:**
1. Open browser console
2. Type: `typeof saveAiModelConfig`
3. Type: `typeof loadAiModelConfig`
4. Type: `typeof getSelectedAiModel`

**Expected:**
- ✅ All return "function"
- ✅ Functions are globally accessible
- ✅ No errors

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 14: Network Requests

**Steps:**
1. Open Network tab in browser DevTools
2. Refresh page
3. Check for all script/CSS files

**Expected:**
- ✅ `style.css` loads (200)
- ✅ `css/components/notification.css` loads (200)
- ✅ `js/utils/storage.js` loads (200)
- ✅ `js/utils/validators.js` loads (200)
- ✅ `js/components/notification.js` loads (200)
- ✅ `js/pages/configurationPage.js` loads (200)
- ✅ `script.js` loads (200)
- ✅ No 404 errors

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

### Test 15: Mobile Responsiveness

**Steps:**
1. Open browser DevTools
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select mobile device (e.g., iPhone 12)
4. Test Configuration tab

**Expected:**
- ✅ Page displays correctly on mobile
- ✅ Dropdown works on mobile
- ✅ Notifications display correctly (full width on mobile)
- ✅ No horizontal scrolling

**Actual:**
- [ ] Pass / [ ] Fail
- Notes: _______________

---

## 📊 Test Summary

| Test | Status | Notes |
|------|--------|-------|
| 1. Page Load | ⏳ | |
| 2. Configuration Display | ⏳ | |
| 3. Old Function | ⏳ | |
| 4. UI Interaction | ⏳ | |
| 5. Model Selection | ⏳ | |
| 6. LocalStorage | ⏳ | |
| 7. Page Reload | ⏳ | |
| 8. New Class | ⏳ | |
| 9. Notifications | ⏳ | |
| 10. Storage Utility | ⏳ | |
| 11. Validators | ⏳ | |
| 12. Tab Switching | ⏳ | |
| 13. Legacy Functions | ⏳ | |
| 14. Network Requests | ⏳ | |
| 15. Mobile | ⏳ | |

**Total Tests:** 15  
**Passed:** ___  
**Failed:** ___  
**Pass Rate:** ___%

---

## 🐛 Issues Found

| Issue # | Description | Severity | Status |
|---------|-------------|----------|--------|
| | | | |

---

## ✅ Sign-Off

- [ ] All tests passed
- [ ] No critical issues
- [ ] Ready for next phase

**Tested By:** _______________  
**Date:** _______________  
**Browser:** _______________  
**OS:** _______________

---

## 🚀 Next Steps

If all tests pass:
1. ✅ Mark Configuration tab migration as complete
2. ✅ Update INCREMENTAL_MIGRATION_GUIDE.md
3. ✅ Begin Executor tab migration

If tests fail:
1. ❌ Document issues
2. ❌ Fix issues
3. ❌ Re-test
4. ❌ Consider rollback if critical
