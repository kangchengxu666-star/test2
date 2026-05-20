from src.cs_bot.products import (
    format_catalog_for_prompt,
    get_all_products,
    get_in_stock_products,
    get_products_by_category,
    search_products,
)


def test_catalog_not_empty():
    assert len(get_all_products()) > 0


def test_all_products_have_required_fields():
    for product in get_all_products():
        assert product.id
        assert product.name
        assert product.category
        assert product.price_usd > 0
        assert product.description


def test_in_stock_products_excludes_out_of_stock():
    in_stock = get_in_stock_products()
    assert all(p.in_stock for p in in_stock)
    # Catalog contains at least one out-of-stock item (Kuromi Duo)
    assert len(in_stock) < len(get_all_products())


def test_get_products_by_category_exact_match():
    plush = get_products_by_category("Plush Toys")
    assert len(plush) > 0
    assert all(p.category == "Plush Toys" for p in plush)


def test_get_products_by_category_case_insensitive():
    plush_lower = get_products_by_category("plush toys")
    plush_upper = get_products_by_category("PLUSH TOYS")
    assert len(plush_lower) == len(plush_upper)


def test_get_products_by_category_unknown_returns_empty():
    result = get_products_by_category("NonExistentCategory")
    assert result == []


def test_search_products_by_name():
    results = search_products("hoodie")
    assert any("Hoodie" in p.name for p in results)


def test_search_products_by_tag():
    results = search_products("keychain")
    assert len(results) > 0


def test_search_products_no_match_returns_empty():
    results = search_products("unicorn_xyz_nonexistent")
    assert results == []


def test_format_catalog_for_prompt_contains_product_names():
    catalog_text = format_catalog_for_prompt()
    assert "Hello Kitty" in catalog_text
    assert "$" in catalog_text


def test_format_catalog_marks_out_of_stock():
    catalog_text = format_catalog_for_prompt()
    assert "OUT OF STOCK" in catalog_text
