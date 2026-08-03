"""
Example usage of Semantic Search Utility
"""

from nlp.semantic_search_util import SemanticSearchEngine, find_similar_row, find_top_k_similar_rows

EXCEL_PATH = r"C:\BLKDeveloper\Synaptix\Rest_API_Data\Swagger_Data_2026_06_07_15_53.xlsx"


def example_1_simple_search():
    """Example 1: Simple search using convenience function"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Search - Get Best Match Sl No")
    print("="*80)

    query = "Create a new pet in the pet store"

    search_columns = ['Component', 'Component_SmallDescription', 'Operation_Method',
                      'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary']

    sl_no = find_similar_row(EXCEL_PATH, query, search_columns=search_columns)
    print(f"\n🔍 Query: '{query}'")
    print(f"📋 Search Columns: {search_columns}")
    print(f"🎯 Example 1 - Best Match Sl_No: {sl_no}")


def example_2_top_k_results():
    """Example 2: Get top K similar results"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Top K Results")
    print("="*80)

    query = "Create a new pet in the pet store"
    top_k = 3

    search_columns = ['Component', 'Component_SmallDescription', 'Operation_Method',
                      'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary']

    results = find_top_k_similar_rows(EXCEL_PATH, query, top_k=top_k, search_columns=search_columns)

    print(f"\n🔍 Query: '{query}'")
    print(f"🔷 Search Columns: {search_columns}")
    print(f"🔷📋 Example 2 - Top {top_k} Results:\n")

    for i, result in enumerate(results, 1):
        print(f"  Result #{i}:")
        print(f"    Sl No: {result['sl_no']}")
        print(f"    Score: {result['score']:.4f}")
        print(f"    Excel Row: {result['excel_row']}")
        print(f"    Data Preview: {list(result['data'].items())[:3]}")
        print()


def example_3_advanced_usage():
    """Example 3: Advanced usage with SemanticSearchEngine class"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Advanced Usage with Custom Configuration")
    print("="*80)

    search_columns = ['Component', 'Component_SmallDescription', 'Operation_Method',
                      'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary']

    engine = SemanticSearchEngine(EXCEL_PATH, search_columns=search_columns)

    print(f"\n📋 Available Columns: {engine.columns}")
    print(f"📊 Total Rows: {len(engine.data)}")

    query = "Create a new pet in the pet store"

    results = engine.search(query, top_k=2)

    print(f"\n🔍 Query: '{query}'")
    print(f"🎯 Example 3 - Best Match:")
    if results:
        best = results[0]
        print(f"  Sl No: {best['sl_no']}")
        print(f"  Similarity Score: {best['score']:.4f}")
        print(f"  Full Data:")
        for key, value in best['data'].items():
            print(f"    {key}: {value}")


def example_4_multiple_queries():
    """Example 4: Multiple queries with reusing the same engine"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Multiple Queries (Efficient Reuse)")
    print("="*80)

    search_columns = ['Component', 'Component_SmallDescription', 'Operation_Method',
                      'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary']

    engine = SemanticSearchEngine(EXCEL_PATH, search_columns=search_columns)

    queries = [
        "authenticate user login",
        "update user profile information",
        "list all products",
        "search for items"
    ]

    print(f"\n📋 Search Columns: {search_columns}")
    print(f"\n🔍 Example 4 Running multiple queries:\n")

    for query in queries:
        sl_no = engine.get_best_match_sl_no(query)
        print(f"  Query: '{query}' → Sl No: {sl_no}")


def example_5_custom_columns():
    """Example 5: Using specific columns for embedding generation"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Custom Column Selection for Embeddings")
    print("="*80)

    search_columns = ['Component', 'Component_SmallDescription', 'Operation_Method',
                      'Operation_Path', 'Operation_Summary', 'Operation_SecondarySummary']

    engine = SemanticSearchEngine(EXCEL_PATH, search_columns=search_columns)

    print(f"\n📋 All Columns: {engine.columns}")
    print(f"📋 Search Columns Used: {search_columns}")

    custom_columns = ['Operation_Summary', 'Operation_Path']

    print(f"\n🔧 Regenerating embeddings with custom columns: {custom_columns}")
    engine.regenerate_embeddings(custom_columns)

    query = "Create a new pet in the pet store"
    sl_no = engine.get_best_match_sl_no(query)

    print(f"\n🔍 Query: '{query}'")
    print(f"🎯 Example 5 - Best Match Sl_No: {sl_no}")


if __name__ == "__main__":
    print("\n" + "🚀 SEMANTIC SEARCH UTILITY - EXAMPLES ".center(80, "="))

    try:
        example_1_simple_search()

        example_2_top_k_results()

        example_3_advanced_usage()

        example_4_multiple_queries()

        example_5_custom_columns()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("✅ Examples completed!")
    print("="*80 + "\n")