# Relationship of daily round correlations to final round correlations

There is a [numerai forum thread](https://forum.numer.ai/t/relationship-of-daily-round-correlations-to-final-round-correlations/1176/1) on the topic, how daily updates of submission results relate to the final results.

Based on that thread, for the **Numerai Crypto Signals Tournament**, here are some practical things to consider:

1. **Are only final day results (30 days after submission) meaningful?**
   - **Yes**, the final results (resolved scores) are the most reliable indicators of model performance. Temporary scores early in a round can vary significantly from the final score.
   
2. **Do early daily scores make sense?**
   - **Somewhat**, but they are less informative early in a round. While early daily scores have some value, they don't reliably predict final outcomes, especially within the first 15 days. On average, early scores have about a 0.02 to 0.03 difference from the final score by the end of a round.

### Insights from the Data:
- **Early Scores' Volatility**:
  - The thread notes that daily scores fluctuate considerably during the first two weeks. Around the 15th day, scores become "somewhat informative," meaning the distance between daily scores and the final score decreases to around 0.01.
  
- **Negative Skew of Early Scores**:
  - Early daily score distances from the final score show a **negative skew**, meaning that initial scores tend to be lower than final scores. This suggests that predictions often improve as the round progresses.

- **Outcome Reversals**:
  - The chance of an "outcome reversal" (i.e., a negative early score becoming positive or vice versa) is around 35% on the first day. This probability drops to around 10% by day 11, implying that the early scores are less reliable but become more indicative of the final outcome as time passes.

### Model Comparisons and Variability:
- **Correlation (CORR) vs. MMC**:
  - It was found that **MMC (meta-model contribution)** scores tend to be more stable over time compared to correlation scores. This makes percentile rankings based on MMC slightly more reliable through the round than those based on correlation.

- **Signals vs. Classic Tournament**:
  - The analysis shows similarities in daily score behavior between Signals and Classic models. However, daily distances (differences from the final score) can vary significantly from round to round, indicating that diversifying strategies between the two tournaments could help reduce risk.

### Takeaways:
1. **Final results matter most**: While early scores can provide some insight, their volatility and the potential for outcome reversals mean that only the final day scores should be trusted for meaningful evaluation.
2. **Expect variability**: Daily score movements are unpredictable, and early positive or negative scores may not reflect the final outcome. By day 15, scores become "somewhat informative."
3. **Outcome Reversal Probability**: There’s a significant chance of score sign reversal early on, but this diminishes rapidly after day 11.
4. **Stability in MMC**: MMC scores tend to be more consistent than CORR scores, which are more prone to volatility, especially in the earlier days of a round. 

This analysis helps to moderate expectations about early daily scores and underscores the importance of waiting for final results before judging model performance.

_Bottomline: with numerai crypto contest, submit your predictions and forget about them for 30 days._
