import yfinance as yf


class FinancialAnalyser:
    """
    Fetches and formats financial trend data for a given stock using yfinance.
    Provides both value series and natural language trend summaries for LLM ingestion.
    """

    def __init__(self) -> None:
        # No initialization required in this version.
        pass

    async def get_financial_trend(self, script: str) -> str:
        """
        Retrieves and summarizes financial metrics (yearly & quarterly) for a given stock.

        Parameters:
            script (str): Stock ticker symbol (e.g., 'RELIANCE.NS').

        Returns:
            str: A combined summary of value series and trend insights for each key metric.
        """

        script = script.upper() + ".NS"
        ticker = yf.Ticker(script)

        # Try fetching income statement data
        try:
            yearly_financials = ticker.financials
            quarterly_financials = ticker.quarterly_financials
        except Exception as e:
            return f"Failed to fetch financial data for {script}: {str(e)}"

        # Return early if there's no financial data
        if yearly_financials.empty and quarterly_financials.empty:
            return f"No financial data available for {script}."

        output = f"Financial trend analysis for {script}:\n\n"

        # Analyze and append yearly trends
        output += "Yearly Performance:\n"
        output += self.__format_trend(yearly_financials, period="year")

        # Analyze and append quarterly trends
        output += "\nQuarterly Performance:\n"
        output += self.__format_trend(quarterly_financials, period="quarter")

        return output.strip()

    def __format_trend(self, df, period="year") -> str:
        """
        Formats both value series and natural-language trend summaries for each metric.

        Parameters:
            df (DataFrame): Financial DataFrame (either yearly or quarterly).
            period (str): Either 'year' or 'quarter' to customize formatting.

        Returns:
            str: Clean, LLM-readable summary of trends per metric.
        """
        if df.empty:
            return "No data available.\n"

        # Transpose to have dates/quarters as rows and metrics as columns
        df = df.transpose().sort_index()

        # Get the last 5 years or last 4 quarters of data
        recent_periods = df.tail(4 if period == "quarter" else 5)

        lines = []

        # Define which metrics to track
        key_metrics = ["Total Revenue", "Gross Profit", "Net Income", "Diluted EPS"]

        # Formatter function to make big numbers more readable
        def fmt(val):
            try:
                if abs(val) >= 1e12:
                    return f"{val/1e12:.2f}T"
                elif abs(val) >= 1e9:
                    return f"{val/1e9:.2f}B"
                elif abs(val) >= 1e6:
                    return f"{val/1e6:.2f}M"
                elif abs(val) >= 1e3:
                    return f"{val/1e3:.2f}K"
                else:
                    return f"{val:.2f}"
            except:
                return "NA"

        # Loop through each metric and extract data
        for metric in key_metrics:
            if metric not in recent_periods.columns:
                continue  # Skip if metric not available

            values = recent_periods[metric].dropna()
            if values.empty:
                continue  # Skip if no data for this metric

            # Format each value for readability
            formatted_values = [fmt(v) for v in values]

            # Determine trend direction from first and last values
            if len(values) >= 2:
                first = values.iloc[0]
                last = values.iloc[-1]
                if last > first:
                    trend = "increased"
                elif last < first:
                    trend = "decreased"
                else:
                    trend = "remained stable"
                summary = f"→ Trend: {trend} from {fmt(first)} to {fmt(last)}"
            else:
                summary = "→ Trend: not enough data to determine"

            # Append the formatted series + trend line
            lines.append(
                f"- {metric} over the last {len(formatted_values)} {period}s: {formatted_values}\n  {summary}"
            )

        return "\n".join(lines) if lines else "Key metrics not found in the data.\n"

if __name__=="__main__":
    import asyncio
    analyser = FinancialAnalyser()
    data = asyncio.run(analyser.get_financial_trend(script="titan"))
    print(data)
