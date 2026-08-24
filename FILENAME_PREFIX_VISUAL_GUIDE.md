# Filename Prefix Feature - Visual Guide

**Feature:** Custom Filename Prefix for OpenAPI Parser and Swagger Scraper

---

## 🎨 UI Layout Comparison

### ❌ BEFORE (Incorrect)

```
┌─────────────────────────────────────────────────────────────────────┐
│  OpenAPI JSON Parser Tab                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Enter file name prefix          ]  ☐ SetDefaultFileName  [▶️ Run] │
│   ↑ Input field FIRST (WRONG!)       ↑ No spaces          ↑ Disabled│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### ✅ AFTER (Correct)

```
┌─────────────────────────────────────────────────────────────────────┐
│  OpenAPI JSON Parser Tab                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ☐ Set Default File Name  [Enter file name prefix          ]  [▶️ Run]│
│  ↑ Checkbox FIRST (CORRECT!)  ↑ Input field SECOND         ↑ Disabled│
│     With spaces!                  Responsive width                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 State Transitions

### State 1: Initial State (Default)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [                              ]  [🔒 Run]│
│  ↑ Unchecked              ↑ Empty                         ↑ DISABLED│
│  ✅ Enabled               ✅ Enabled                                 │
└─────────────────────────────────────────────────────────────────────┘

User Action: None
Button State: 🔒 DISABLED (Cannot click)
```

---

### State 2: User Checks Checkbox

```
USER CLICKS CHECKBOX
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ☑ Set Default File Name  [                              ]  [✅ Run]│
│  ↑ CHECKED                ↑ Empty                         ↑ ENABLED │
│  ✅ Enabled               🔒 DISABLED (grayed out)                   │
└─────────────────────────────────────────────────────────────────────┘

User Action: Checked checkbox
Button State: ✅ ENABLED (Can click)
Input State: 🔒 DISABLED (Cannot type)

When submitted: OpenAPI_Data_2026_08_25_14_30.xlsx
```

---

### State 3: User Enters Custom Text

```
USER TYPES "MyCustomAPI"
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [MyCustomAPI                   ]  [✅ Run]│
│  ↑ Unchecked              ↑ Has text                      ↑ ENABLED │
│  🔒 DISABLED              ✅ Enabled                                 │
└─────────────────────────────────────────────────────────────────────┘

User Action: Entered text in input field
Button State: ✅ ENABLED (Can click)
Checkbox State: 🔒 DISABLED (Cannot check)

When submitted: MyCustomAPI_2026_08_25_14_35.xlsx
```

---

### State 4: User Clears Text

```
USER DELETES ALL TEXT
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [                              ]  [🔒 Run]│
│  ↑ Unchecked              ↑ Empty                         ↑ DISABLED│
│  ✅ Enabled               ✅ Enabled                                 │
└─────────────────────────────────────────────────────────────────────┘

User Action: Cleared text from input field
Button State: 🔒 DISABLED (Cannot click)
Checkbox State: ✅ ENABLED (Can check again)

Back to initial state!
```

---

## 📊 State Diagram

```
                    ┌─────────────────────┐
                    │   INITIAL STATE     │
                    │                     │
                    │  ☐ Checkbox         │
                    │  [ ] Input (empty)  │
                    │  🔒 Button DISABLED │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        User checks checkbox         User enters text
                │                             │
                ▼                             ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │  CHECKBOX CHECKED   │       │   TEXT ENTERED      │
    │                     │       │                     │
    │  ☑ Checkbox         │       │  ☐ Checkbox         │
    │  🔒 Input DISABLED  │       │  [Text] Input       │
    │  ✅ Button ENABLED  │       │  ✅ Button ENABLED  │
    └──────────┬──────────┘       └──────────┬──────────┘
               │                             │
        User unchecks             User clears text
               │                             │
               └──────────────┬──────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   INITIAL STATE     │
                    │  (Back to start)    │
                    └─────────────────────┘
```

---

## 🎯 Behavior Matrix

| Checkbox | Input Field | Button | Filename Format |
|----------|-------------|--------|-----------------|
| ☐ Unchecked | Empty | 🔒 Disabled | N/A (cannot submit) |
| ☑ Checked | 🔒 Disabled | ✅ Enabled | `OpenAPI_Data_<timestamp>.xlsx` |
| 🔒 Disabled | "MyAPI" | ✅ Enabled | `MyAPI_<timestamp>.xlsx` |
| ☐ Unchecked | "CustomAPI" | ✅ Enabled | `CustomAPI_<timestamp>.xlsx` |

---

## 📝 User Workflows

### Workflow 1: Use Default Filename

```
Step 1: User opens OpenAPI Parser tab
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [        ]  [🔒 Run] │
        └─────────────────────────────────────────────────┘

Step 2: User checks "Set Default File Name"
        ┌─────────────────────────────────────────────────┐
        │  ☑ Set Default File Name  [        ]  [✅ Run] │
        │                           ↑ Disabled            │
        └─────────────────────────────────────────────────┘

Step 3: User enters URL and clicks "Run JSON Parser"
        ↓
        Result: OpenAPI_Data_2026_08_25_14_30.xlsx
```

---

### Workflow 2: Use Custom Filename

```
Step 1: User opens OpenAPI Parser tab
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [        ]  [🔒 Run] │
        └─────────────────────────────────────────────────┘

Step 2: User types "PetStore_API" in input field
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [PetStore_API]  [✅ Run]│
        │  ↑ Disabled                                     │
        └─────────────────────────────────────────────────┘

Step 3: User enters URL and clicks "Run JSON Parser"
        ↓
        Result: PetStore_API_2026_08_25_14_35.xlsx
```

---

### Workflow 3: Change Mind (Checkbox → Custom)

```
Step 1: User checks checkbox
        ┌─────────────────────────────────────────────────┐
        │  ☑ Set Default File Name  [        ]  [✅ Run] │
        └─────────────────────────────────────────────────┘

Step 2: User changes mind, unchecks checkbox
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [        ]  [🔒 Run] │
        └─────────────────────────────────────────────────┘

Step 3: User types custom prefix
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [MyAPI]  [✅ Run]    │
        │  ↑ Disabled                                     │
        └─────────────────────────────────────────────────┘

Step 4: User submits
        ↓
        Result: MyAPI_2026_08_25_14_40.xlsx
```

---

### Workflow 4: Change Mind (Custom → Checkbox)

```
Step 1: User types custom prefix
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [MyAPI]  [✅ Run]    │
        │  ↑ Disabled                                     │
        └─────────────────────────────────────────────────┘

Step 2: User changes mind, clears text
        ┌─────────────────────────────────────────────────┐
        │  ☐ Set Default File Name  [        ]  [🔒 Run] │
        │  ↑ Enabled again                                │
        └─────────────────────────────────────────────────┘

Step 3: User checks checkbox
        ┌─────────────────────────────────────────────────┐
        │  ☑ Set Default File Name  [        ]  [✅ Run] │
        └─────────────────────────────────────────────────┘

Step 4: User submits
        ↓
        Result: OpenAPI_Data_2026_08_25_14_45.xlsx
```

---

## 🔍 Detailed Component States

### Checkbox States

| State | Visual | Enabled? | Can Click? |
|-------|--------|----------|------------|
| Unchecked, Input Empty | ☐ | ✅ Yes | ✅ Yes |
| Checked | ☑ | ✅ Yes | ✅ Yes (to uncheck) |
| Unchecked, Input Has Text | ☐ | 🔒 No | ❌ No |

### Input Field States

| State | Visual | Enabled? | Can Type? |
|-------|--------|----------|-----------|
| Checkbox Unchecked | `[                ]` | ✅ Yes | ✅ Yes |
| Checkbox Checked | `[                ]` | 🔒 No | ❌ No |
| Has Text | `[MyCustomAPI     ]` | ✅ Yes | ✅ Yes |

### Button States

| State | Visual | Enabled? | Can Click? |
|-------|--------|----------|------------|
| Initial (Both Empty) | `[🔒 Run]` | 🔒 No | ❌ No |
| Checkbox Checked | `[✅ Run]` | ✅ Yes | ✅ Yes |
| Input Has Text | `[✅ Run]` | ✅ Yes | ✅ Yes |

---

## 📂 Filename Examples

### OpenAPI Parser

| Scenario | Filename |
|----------|----------|
| Default (Checkbox) | `OpenAPI_Data_2026_08_25_14_30.xlsx` |
| Custom: "PetStore" | `PetStore_2026_08_25_14_35.xlsx` |
| Custom: "MyAPI_v2" | `MyAPI_v2_2026_08_25_14_40.xlsx` |
| Custom: "Test_Export" | `Test_Export_2026_08_25_14_45.xlsx` |

### Swagger Scraper

| Scenario | Filename |
|----------|----------|
| Default (Checkbox) | `Swagger_Data_2026_08_25_15_00.xlsx` |
| Custom: "SwaggerUI" | `SwaggerUI_2026_08_25_15_05.xlsx` |
| Custom: "API_Docs" | `API_Docs_2026_08_25_15_10.xlsx` |
| Custom: "Export_2024" | `Export_2024_2026_08_25_15_15.xlsx` |

---

## 🎨 Visual Mockup

### OpenAPI Parser Tab - Full View

```
┌───────────────────────────────────────────────────────────────────────┐
│                         OpenAPI JSON Parser                           │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Directly parses the OpenAPI/Swagger JSON specification.             │
│  ✅ Fast (~1 second)                                                  │
│  ✅ No browser required                                               │
│  ✅ More reliable                                                     │
│                                                                        │
│  OpenAPI Spec URL:                                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ https://petstore.swagger.io/v2/swagger.json                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                        │
│                         — OR —                                        │
│                                                                        │
│  Upload OpenAPI JSON File:                                            │
│  [Choose File] No file chosen                                        │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ ☐ Set Default File Name  [Enter file name prefix    ]  [▶️ Run]│ │
│  │ ↑ Checkbox               ↑ Input field              ↑ Button   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
```

### Swagger Scraper Tab - Full View

```
┌───────────────────────────────────────────────────────────────────────┐
│                         Swagger UI Scraper                            │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Extracts data by scraping the Swagger UI interface using browser    │
│  automation.                                                          │
│  ✅ Works when only UI is accessible                                  │
│  ⚠️ Slower (1-5 minutes)                                              │
│  ⚠️ Requires browser automation                                       │
│                                                                        │
│  Swagger UI URL:                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ https://petstore.swagger.io/                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ ☐ Set Default File Name  [Enter file name prefix    ]  [▶️ Run]│ │
│  │ ↑ Checkbox               ↑ Input field              ↑ Button   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing Scenarios

### Scenario A: Rapid Toggling

```
Step 1: Check checkbox
        ☑ Set Default File Name  [        ]  [✅ Run]

Step 2: Uncheck checkbox
        ☐ Set Default File Name  [        ]  [🔒 Run]

Step 3: Type text
        ☐ Set Default File Name  [MyAPI]  [✅ Run]
        ↑ Disabled

Step 4: Clear text
        ☐ Set Default File Name  [        ]  [🔒 Run]
        ↑ Enabled again

Step 5: Check checkbox again
        ☑ Set Default File Name  [        ]  [✅ Run]

Result: ✅ All transitions work smoothly
```

---

### Scenario B: Edge Cases

#### Edge Case 1: Whitespace Only
```
User types: "   " (spaces only)
Result: Treated as empty, button disabled ✅
```

#### Edge Case 2: Special Characters
```
User types: "My-API_v2.0"
Result: Accepted, filename: My-API_v2.0_2026_08_25_14_30.xlsx ✅
```

#### Edge Case 3: Very Long Prefix
```
User types: "VeryLongCustomPrefixForTestingPurposes"
Result: Accepted, filename: VeryLongCustomPrefixForTestingPurposes_2026_08_25_14_30.xlsx ✅
```

---

## ✅ Verification Checklist

### Visual Layout
- [x] Checkbox is on the LEFT
- [x] Input field is AFTER checkbox
- [x] Button is on the RIGHT
- [x] Label text has spaces: "Set Default File Name"
- [x] Input field is responsive (flex: 1, min-width: 200px)

### Functionality
- [x] Button disabled by default
- [x] Checking checkbox enables button and disables input
- [x] Entering text enables button and disables checkbox
- [x] Clearing text re-enables checkbox and disables button
- [x] Unchecking checkbox disables button (if input empty)

### Filename Generation
- [x] Default format: `OpenAPI_Data_YYYY_MM_DD_HH_MM.xlsx`
- [x] Custom format: `<custom_prefix>_YYYY_MM_DD_HH_MM.xlsx`
- [x] Timestamp is always appended
- [x] No duplicate underscores

---

## 🎉 Conclusion

The filename prefix feature is now **fully functional and correctly implemented** with:

1. ✅ Correct UI layout (Checkbox → Input → Button)
2. ✅ Proper label text with spaces
3. ✅ Correct control logic (mutual exclusivity)
4. ✅ Correct filename generation
5. ✅ Responsive design
6. ✅ All edge cases handled

**Status:** Ready for production! 🚀

---

**Created By:** Devin AI  
**Date:** August 25, 2026  
**Version:** 1.0
