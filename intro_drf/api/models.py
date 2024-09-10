from django.db import models

# Create your models here.

class Institutions(models.Model):
    symbol = models.TextField(primary_key=True)
    updated_on = models.TextField(blank=True, null=True)
    net_transaction = models.IntegerField(blank=True, null=True)
    top_sellers = models.JSONField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    top_buyers = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'institutions'


class Metadata(models.Model):
    sector = models.TextField(blank=True, null=True)
    sub_sector = models.TextField(blank=True, null=True)
    slug = models.TextField(primary_key=True)
    sub_sector_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata'


class Reports(models.Model):
    sub_sector = models.TextField(primary_key=True)
    total_companies = models.TextField(blank=True, null=True)
    total_market_cap = models.TextField(blank=True, null=True)
    avg_market_cap = models.TextField(blank=True, null=True)
    filtered_median_pe = models.TextField(blank=True, null=True)
    filtered_weighted_avg_pe = models.TextField(blank=True, null=True)
    min_company_pe = models.TextField(blank=True, null=True)
    max_company_pe = models.TextField(blank=True, null=True)
    avg_yoy_q_earnings_growth = models.TextField(blank=True, null=True)
    avg_yoy_q_revenue_growth = models.TextField(blank=True, null=True)
    weighted_max_drawdown = models.TextField(blank=True, null=True)
    weighted_rsd_close = models.TextField(blank=True, null=True)
    median_yield_ttm = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'