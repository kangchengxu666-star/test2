SHIPPING_POLICY = """
## Shipping Policy

**Processing Time:** 1-3 business days after order confirmation.

**Shipping Options & Estimated Delivery:**
| Region              | Standard (Free ≥$35) | Expedited         |
|---------------------|----------------------|-------------------|
| United States       | 7-14 business days   | 3-5 business days |
| United Kingdom      | 10-18 business days  | 5-8 business days |
| Canada              | 10-18 business days  | 5-8 business days |
| Australia/NZ        | 12-20 business days  | 6-10 business days|
| Europe (other)      | 12-20 business days  | 7-12 business days|
| Southeast Asia      | 7-14 business days   | 3-5 business days |
| Other regions       | 15-25 business days  | Contact us        |

**Shipping Costs:**
- Standard shipping: FREE on orders $35+, otherwise $4.99
- Expedited shipping: $12.99 flat rate

**Tracking:** A tracking number is emailed within 24 hours of shipment.

**Customs & Duties:** International buyers may be subject to customs fees.
We are not responsible for delays due to customs clearance.
"""

RETURN_POLICY = """
## Return & Exchange Policy

**Return Window:** 30 days from the date of delivery.

**Eligible for Return:**
- Items in original, unused condition with tags attached
- Damaged or defective items (contact us within 7 days of receipt)
- Wrong item received

**NOT Eligible for Return:**
- Items marked "Final Sale" or "Limited Edition"
- Out-of-stock items that were back-ordered and received

**How to Return:**
1. Contact our support with your order number and reason
2. We will provide a prepaid return label (for US orders)
3. International customers cover return shipping costs
4. Refund processed within 5-7 business days after we receive the item

**Exchanges:**
- Exchanges are available for size/color issues
- Subject to availability — if the item is out of stock, a refund will be issued

**Refund Method:**
- Original payment method only
- Shipping fees are non-refundable (except for our errors)
"""

FAQ = """
## Frequently Asked Questions

**Q: Are your products officially licensed?**
A: Yes! All Hello Kitty products are officially licensed by Sanrio.

**Q: Do you offer gift wrapping?**
A: Yes! Add "gift wrap" to your order notes at checkout. Free of charge.

**Q: Can I cancel or modify my order?**
A: Orders can be cancelled/modified within 2 hours of placement.
   After that, the order may have already been processed.

**Q: What if my package is lost?**
A: If tracking shows no movement for 10+ business days, contact us.
   We will reship or refund based on the situation.

**Q: Do you restock out-of-stock items?**
A: We regularly restock popular items. Follow our TikTok shop for restock alerts.

**Q: Is there a size guide for apparel?**
A: Yes — sizes run slightly small, we recommend sizing up one size.
   XS: US 0-2, S: US 4-6, M: US 8-10, L: US 12-14, XL: US 16-18, 2XL: US 20-22, 3XL: US 24-26
"""


def get_all_policies() -> str:
    return "\n".join([SHIPPING_POLICY, RETURN_POLICY, FAQ])
