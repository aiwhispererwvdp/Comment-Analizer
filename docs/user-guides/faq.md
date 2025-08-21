# Frequently Asked Questions (FAQ)

## 🚀 Getting Started Questions

### Q: What do I need to use this system?
**A:** You need:
- Computer with Python 3.8+ installed
- Internet connection for AI analysis
- OpenAI API key (create account at platform.openai.com)
- Customer comments data in Excel, CSV, JSON, or TXT format

### Q: How much does it cost to analyze comments?
**A:** Costs depend on the number of comments:
- **Typical cost**: $0.002 per comment (about $2 for 1,000 comments)
- **Sample analysis** (50 comments): ~$0.10
- **Small dataset** (500 comments): ~$1.00
- **Large dataset** (5,000 comments): ~$10.00

The system shows cost estimates before you start analysis.

### Q: What file formats are supported?
**A:** The system supports:
- **Excel (.xlsx)** - Recommended for most users
- **CSV (.csv)** - Universal compatibility
- **JSON (.json)** - For API integrations
- **Text (.txt)** - Simple comment lists

### Q: How long does analysis take?
**A:** Analysis speed depends on dataset size:
- **50 comments**: 1-2 minutes
- **500 comments**: 5-10 minutes  
- **2,000 comments**: 15-30 minutes
- **5,000+ comments**: 30-60 minutes

## 📊 Data and Analysis Questions

### Q: What languages does the system support?
**A:** The system natively supports:
- **Spanish** (including Paraguayan dialect)
- **Guaraní** (with automatic translation to Spanish)
- **Mixed language** comments (code-switching)

### Q: How accurate is the sentiment analysis?
**A:** The system achieves:
- **90%+ accuracy** for clear Spanish text
- **85%+ accuracy** for translated Guaraní text
- **80%+ accuracy** for mixed language content

Accuracy varies based on comment clarity and context.

### Q: What if my data has personal information?
**A:** **Remove personal information before upload**:
- Customer names, phone numbers, addresses
- Email addresses and account numbers
- Any sensitive personal data

The system analyzes text content only - personal data isn't needed for analysis.

### Q: Can I analyze comments about other topics besides telecommunications?
**A:** Yes! While optimized for telecommunications, the system works for:
- Any customer feedback or reviews
- Employee feedback and surveys
- Social media comments
- Support ticket analysis
- Product reviews

### Q: What's the difference between analysis types?
**A:** Three analysis depths available:
- **Basic**: Sentiment only (fastest, cheapest)
- **Standard**: Sentiment + themes (recommended)
- **Comprehensive**: Full analysis with emotions (most detailed)

## 🔧 Technical Questions

### Q: Why can't I upload my file?
**A:** Common file upload issues:
- **File too large**: Limit is 200MB (split large files)
- **Unsupported format**: Use Excel, CSV, JSON, or TXT
- **Corrupted file**: Re-save your file and try again
- **Special characters**: Remove special characters from filename

### Q: What does "Low Confidence" mean in results?
**A:** Confidence scores indicate analysis certainty:
- **90-100%**: Highly reliable
- **80-89%**: Very reliable
- **70-79%**: Generally reliable
- **60-69%**: Needs review
- **Below 60%**: Uncertain, requires manual check

Low confidence usually means unclear or ambiguous comments.

### Q: Can I run this on my phone or tablet?
**A:** The system has a mobile-responsive interface:
- **Smartphones**: Basic functionality available
- **Tablets**: Full functionality with touch interface
- **Best experience**: Desktop or laptop computers

### Q: How do I save my analysis results?
**A:** Multiple export options available:
- **Excel**: Complete report with charts (recommended)
- **CSV**: Raw data for further analysis
- **Summary**: Executive summary in text format
- **JSON**: Machine-readable data

### Q: What if the analysis stops or fails?
**A:** Recovery options:
- **Resume processing**: Continue from where it stopped
- **Partial results**: Access already processed data
- **Retry**: Start over with different settings
- **Reduce batch size**: Use smaller batches for stability

## 💰 Cost and Budget Questions

### Q: How can I control costs?
**A:** Built-in cost control features:
- **Set daily budgets**: Automatic spending limits
- **Real-time tracking**: Live cost monitoring
- **Sample analysis**: Test with small datasets first
- **Duplicate detection**: Avoid analyzing duplicate comments

### Q: What if I exceed my budget?
**A:** Safety features prevent overspending:
- **Automatic stops**: Analysis stops at budget limit
- **Alerts**: Warnings at 75% and 90% of budget
- **Approval required**: Manual approval for budget overruns

### Q: Can I get a cost estimate before analysis?
**A:** Yes! The system provides:
- **Pre-analysis estimates**: Cost prediction before starting
- **Real-time costs**: Live tracking during analysis
- **Historical analytics**: Previous analysis costs

## 📈 Results and Reporting Questions

### Q: How do I interpret the sentiment results?
**A:** Sentiment classifications:
- **Positive**: Customer satisfaction, praise, recommendations
- **Negative**: Complaints, problems, frustrations  
- **Neutral**: Factual statements, informational content

Look at the percentage distribution and individual comment details.

### Q: What are "themes" in the results?
**A:** Themes are topics customers discuss:
- **Internet Speed**: Connection speed issues/praise
- **Customer Service**: Support interaction feedback
- **Pricing**: Cost and billing concerns
- **Installation**: Setup and installation experience
- **Technical Issues**: Equipment and connection problems

### Q: How do I use results for business decisions?
**A:** Focus on:
- **Top pain points**: Issues affecting most customers
- **Satisfaction trends**: Changes over time
- **Priority matrix**: High impact + high frequency issues first
- **Success indicators**: Positive themes to leverage

### Q: Can I share results with my team?
**A:** Yes! Export options for sharing:
- **Excel reports**: Professional format for executives
- **Summary reports**: Key findings for quick review
- **Raw data**: Detailed analysis for technical teams
- **Presentations**: Charts and graphs for meetings

## 🔍 Troubleshooting Questions

### Q: The application won't start - what should I do?
**A:** Try these steps:
1. **Check Python version**: `python --version` (need 3.8+)
2. **Reinstall dependencies**: `pip install -r requirements.txt`
3. **Check API key**: Verify your `.env` file is correct
4. **Try different port**: `streamlit run src/main.py --server.port 8502`

### Q: Analysis results seem wrong - what can I do?
**A:** Verification steps:
1. **Check confidence scores**: Low scores indicate uncertain results
2. **Review individual comments**: Look at detailed analysis
3. **Try comprehensive analysis**: More detailed analysis mode
4. **Manual review**: Use the manual review feature for corrections

### Q: The system is running slowly - how can I speed it up?
**A:** Performance optimization:
1. **Reduce batch size**: Use 50-100 comments per batch
2. **Close browser tabs**: Free up memory
3. **Use smaller samples**: Test with fewer comments first
4. **Check internet**: Ensure stable connection

### Q: I'm getting API errors - what's wrong?
**A:** Common API issues:
1. **Invalid key**: Check your OpenAI API key is correct
2. **No credits**: Ensure your OpenAI account has available credits
3. **Rate limits**: Analysis may pause due to API limits (normal)
4. **Network issues**: Check your internet connection

## 📚 Advanced Usage Questions

### Q: Can I schedule automatic analysis?
**A:** Currently manual operation only. Planned features:
- Automated weekly/monthly analysis
- Email reports
- Integration with business systems

### Q: Can I customize the analysis for my business?
**A:** Customization options:
- **Analysis depth**: Choose basic, standard, or comprehensive
- **Language settings**: Optimize for your customer languages
- **Theme focus**: Emphasize telecommunications themes
- **Report branding**: Add company logo and colors

### Q: How do I analyze trends over time?
**A:** For trend analysis:
- **Include dates**: Upload data with date columns
- **Multiple time periods**: Analyze different months separately
- **Compare results**: Use Excel to compare period reports
- **Look for patterns**: Identify seasonal or event-related changes

### Q: Can I integrate this with other systems?
**A:** Integration options:
- **Export formats**: CSV, JSON for data import
- **API access**: Contact support for API integration
- **Database export**: Import results into business intelligence tools

## 🤝 Support Questions

### Q: How do I get help if I'm stuck?
**A:** Support resources:
1. **User Manual**: Complete documentation available
2. **Troubleshooting Guide**: Common problem solutions
3. **Email Support**: support@personal.com.py
4. **Training**: Request user training sessions

### Q: Can I request new features?
**A:** Yes! We welcome feedback:
- Submit feature requests through support
- Participate in user feedback sessions
- Join beta testing programs for new features

### Q: Is training available?
**A:** Training options:
- **Self-paced**: Online documentation and tutorials
- **Group sessions**: Monthly training workshops
- **One-on-one**: Individual training available
- **Custom training**: Tailored for your organization

### Q: What if I find a bug or error?
**A:** Report issues:
- Document the exact error message
- Include steps to reproduce the problem
- Send to support@personal.com.py
- Include system information (browser, OS)

---

## 🆘 Still Need Help?

If your question isn't answered here:

1. **Check the [User Manual](user-manual.md)** for detailed information
2. **Review [Troubleshooting Guide](../deployment/troubleshooting.md)** for technical issues  
3. **Contact Support** at support@personal.com.py
4. **Request Training** for hands-on assistance

**We're here to help you succeed with customer feedback analysis!** 🎯