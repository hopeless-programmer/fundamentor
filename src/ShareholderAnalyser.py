import pandas as pd
from config.common_configs import options


class ShareholderAnalyser:
    """
    A class to analyze investor data for a specific stock (script).
    
    It loads investor-level holdings and computes how important a specific stock
    is in the overall portfolio of each investor who has invested in it.
    """

    def __init__(self) -> None:
        """
        Initializes the InvestorAnalyser by loading the investor dataset from CSV.
        """
        self.__investors_data_df: pd.DataFrame = pd.read_csv(options["investors_data_csv"])

    async def get_investor_data(self, script: str) -> str:
        """
        Retrieves and summarizes how much each investor has invested in the given stock,
        and what portion of their total portfolio this investment represents.

        Parameters:
            script (str): The stock symbol to analyze.

        Returns:
            str: A formatted summary of each investor’s allocation to the stock.
        """
        script = script.upper()
        
        # Filter dataset for the given script
        script_investors_df = self.__investors_data_df[
            self.__investors_data_df["Script"] == script
        ]

        if script_investors_df.empty:
            return f"No investors found for {script}."

        # Initialize output summary
        summary = f"Investors in {script} and their portfolio allocation:\n\n"

        # Process each investor who has invested in the given script
        for _, row in script_investors_df.iterrows():
            investor_name = row["Investor"]
            investment_in_script = row["Amount Invested (in Cr)"]

            # Get the full portfolio of this investor
            investor_portfolio_df = self.__investors_data_df[
                self.__investors_data_df["Investor"] == investor_name
            ]

            total_investment = investor_portfolio_df["Amount Invested (in Cr)"].sum()

            # Calculate allocation percentage to the current script
            allocation_pct = round((investment_in_script / total_investment) * 100, 1)

            # Append formatted investor details
            summary += (
                f"Investor: {investor_name}\n"
                f"- Total Portfolio Investment: ₹{total_investment:.1f} Cr\n"
                f"- Investment in {script}: ₹{investment_in_script:.1f} Cr\n"
                f"- Allocation to {script}: {allocation_pct}%\n\n"
            )

        return summary.strip()






if __name__=="__main__":
    import asyncio
    analyser = ShareholderAnalyser()
    data = asyncio.run(analyser.get_investor_data(script="titan"))
    print(data)
