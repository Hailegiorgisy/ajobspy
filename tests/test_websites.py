"""Tests for website scrapers."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd
from ajobspy.model import JobType


class TestEthioJobsScraper:
    """Test EthioJobs.net scraper."""

    @patch('requests.get')
    def test_scrape_ethiojobs_success(self, mock_get, sample_next_data_json):
        """Test successful scraping from EthioJobs."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = f"""
        <html>
            <script id="__NEXT_DATA__" type="application/json">
            {str(sample_next_data_json).replace("'", '"')}
            </script>
        </html>
        """
        mock_get.return_value = mock_response

        try:
            from ajobspy.websites.ethiojobs import scrape_ethiojobs
            
            result = scrape_ethiojobs(search_term="Developer", results_wanted=10)
            
            assert isinstance(result, pd.DataFrame)
            mock_get.assert_called_once()
        except ImportError:
            pytest.skip("EthioJobs scraper not implemented")

    @patch('requests.get')
    def test_scrape_ethiojobs_with_location(self, mock_get):
        """Test scraping with location filter."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        try:
            from ajobspy.websites.ethiojobs import scrape_ethiojobs
            
            result = scrape_ethiojobs(
                search_term="Developer",
                location="Addis Ababa",
                results_wanted=5
            )
            
            assert isinstance(result, pd.DataFrame)
            mock_get.assert_called()
        except ImportError:
            pytest.skip("EthioJobs scraper not implemented")

    @patch('requests.get')
    def test_scrape_ethiojobs_timeout(self, mock_get):
        """Test scraping with request timeout."""
        mock_get.side_effect = TimeoutError("Request timeout")

        try:
            from ajobspy.websites.ethiojobs import scrape_ethiojobs
            
            with pytest.raises(TimeoutError):
                scrape_ethiojobs(search_term="Developer")
        except ImportError:
            pytest.skip("EthioJobs scraper not implemented")


class TestWuzzufScraper:
    """Test Wuzzuf.net scraper."""

    @patch('requests.get')
    def test_scrape_wuzzuf_basic(self, mock_get, sample_html_response):
        """Test basic Wuzzuf scraping."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = sample_html_response
        mock_get.return_value = mock_response

        try:
            from ajobspy.websites.wuzzuf import scrape_wuzzuf
            
            result = scrape_wuzzuf(search_term="Developer", results_wanted=10)
            
            assert isinstance(result, pd.DataFrame)
            mock_get.assert_called()
        except ImportError:
            pytest.skip("Wuzzuf scraper not implemented")


class TestBaytScraper:
    """Test Bayt.com scraper."""

    @patch('requests.get')
    def test_scrape_bayt_basic(self, mock_get):
        """Test basic Bayt scraping."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><div class='job'><h2>Job Title</h2></div></html>"
        mock_get.return_value = mock_response

        try:
            from ajobspy.websites.bayt import scrape_bayt
            
            result = scrape_bayt(search_term="Engineer", results_wanted=10)
            
            assert isinstance(result, pd.DataFrame)
        except ImportError:
            pytest.skip("Bayt scraper not implemented")


class TestJobbermannScraper:
    """Test Jobberman scraper."""

    @patch('requests.get')
    def test_scrape_jobberman_basic(self, mock_get):
        """Test basic Jobberman scraping."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        try:
            from ajobspy.websites.jobberman import scrape_jobberman
            
            result = scrape_jobberman(search_term="Developer", results_wanted=10)
            
            assert isinstance(result, pd.DataFrame)
        except ImportError:
            pytest.skip("Jobberman scraper not implemented")


class TestScraperDataFrame:
    """Test DataFrame output from scrapers."""

    def test_dataframe_has_required_columns(self, sample_jobs_list):
        """Test that returned DataFrame has required columns."""
        df = pd.DataFrame([job.model_dump() for job in sample_jobs_list])
        
        required_columns = ['id', 'title', 'company', 'location', 'job_url', 'site']
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"

    def test_dataframe_deduplication(self, sample_jobs_list):
        """Test deduplication of job URLs in DataFrame."""
        jobs_with_duplicate = sample_jobs_list + [sample_jobs_list[0]]
        df = pd.DataFrame([job.model_dump() for job in jobs_with_duplicate])
        
        df_deduped = df.drop_duplicates(subset=['job_url'])
        
        assert len(df_deduped) < len(df)

    def test_dataframe_to_csv(self, sample_jobs_list, tmp_path):
        """Test exporting DataFrame to CSV."""
        df = pd.DataFrame([job.model_dump() for job in sample_jobs_list])
        
        csv_file = tmp_path / "jobs.csv"
        df.to_csv(csv_file, index=False)
        
        assert csv_file.exists()
        loaded_df = pd.read_csv(csv_file)
        assert len(loaded_df) == len(df)

    def test_dataframe_sorting_by_date(self, sample_jobs_list):
        """Test sorting jobs by date."""
        df = pd.DataFrame([job.model_dump() for job in sample_jobs_list])
        
        df['date_posted'] = pd.to_datetime(df['date_posted'], utc=True)
        df_sorted = df.sort_values('date_posted', ascending=False)
        
        assert df_sorted.iloc[0]['id'] == 'test_001'


class TestScraperRobustness:
    """Test scraper robustness and error handling."""

    @patch('requests.get')
    def test_scraper_respects_timeout(self, mock_get):
        """Test that scraper uses timeout parameter."""
        mock_get.return_value = MagicMock(status_code=200, text="<html></html>")

        try:
            from ajobspy.websites.ethiojobs import scrape_ethiojobs
            
            scrape_ethiojobs(search_term="Developer")
            
            assert mock_get.called
            call_kwargs = mock_get.call_args[1]
            assert 'timeout' in call_kwargs
            assert call_kwargs['timeout'] == 15
        except ImportError:
            pytest.skip("EthioJobs scraper not implemented")
