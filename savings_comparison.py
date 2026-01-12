import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# CONFIGURATION
# ==========================================
YEAR_DAYS = 365

def calculate_yearly_savings(num_cycles, year_days=365):
    """
    Splits the year into 'num_cycles' chunks and calculates total savings.
    Assumes standard reset: Start at 1, increment by 1.
    """
    # 1. Determine the length of each cycle
    # Evenly distribute the remainder days
    # e.g. 365 days, 2 cycles -> 183, 182
    base_length = year_days // num_cycles
    remainder = year_days % num_cycles
    
    lengths = []
    for i in range(num_cycles):
        if i < remainder:
            lengths.append(base_length + 1)
        else:
            lengths.append(base_length)
            
    # 2. Calculate savings for each cycle
    grand_total = 0
    
    # Formula for sum 1..n is n*(n+1)/2
    for lgth in lengths:
        cycle_sum = (lgth * (lgth + 1)) / 2
        grand_total += cycle_sum
        
    return grand_total, lengths

def generate_comparison_data(target_cycles, year_days=365):
    data = []
    
    cycle_labels = {
        1: "Yearly (1)",
        2: "Semi-Annual (2)",
        4: "Quarterly (4)",
        6: "Bi-Monthly (6)",
        12: "Monthly (12)",
        24: "Semi-Monthly (24)",
        26: "Bi-Weekly (26)",
        52: "Weekly (52)",
        365: "Daily (365)"
    }

    for c in target_cycles:
        total, lengths = calculate_yearly_savings(c, year_days)
        
        # Description for tooltip
        desc = f"{lengths[0]} days"
        if len(set(lengths)) > 1:
            desc = f"~{int(np.mean(lengths))} days"
            
        data.append({
            'CyclesPerYear': c,
            'Label': cycle_labels.get(c, str(c)),
            'TotalSavings': total,
            'TotalCouple': total * 2,
            'MaxDailyAmount': max(lengths),
            'AvgDaysPerCycle': year_days / c,
            'Desc': desc
        })
        
    # --- Add Alternative Strategies ---
    # 1. Fixed Daily Amount (to match the ~66k goal)
    # 66795 / 365 = ~183. Let's say 183.
    fixed_daily = 183
    data.append({
        'CyclesPerYear': 0, # Special ID
        'Label': "Fixed Daily (183฿)",
        'TotalSavings': fixed_daily * 365,
        'TotalCouple': (fixed_daily * 365) * 2,
        'MaxDailyAmount': fixed_daily,
        'AvgDaysPerCycle': 0,
        'Desc': "Pay same amount every day"
    })

    # 2. 52-Week Challenge (x50)
    # Week 1 = 50, Week 2 = 100 ... Week 52 = 2600
    weeks = 52
    week_amounts = [50 * i for i in range(1, weeks + 1)] # 50, 100... 2600
    w_total = sum(week_amounts) # 50 * 1378 = 68900
    data.append({
        'CyclesPerYear': 0,
        'Label': "52-Week Challenge (x50)",
        'TotalSavings': w_total,
        'TotalCouple': w_total * 2,
        'MaxDailyAmount': 2600, # Very hard at end of year
        'AvgDaysPerCycle': 7,
        'Desc': "Wk1=50, Wk52=2600"
    })

    # 3. Weekday Ladder
    # Mon=50, Tue=100 ... Sun=350. (Sum=1400/week)
    ladder_week_total = sum([50 * i for i in range(1, 8)]) # 1400
    ladder_year_total = ladder_week_total * 52 # 72800
    data.append({
        'CyclesPerYear': 0,
        'Label': "Weekday Ladder",
        'TotalSavings': ladder_year_total,
        'TotalCouple': ladder_year_total * 2,
        'MaxDailyAmount': 350,
        'AvgDaysPerCycle': 0,
        'Desc': "Mon=50...Sun=350"
    })
    
    # --- New Pitch Strategies ---
    
    # 4. Reverse 52-Week (Front-Loaded)
    # Psychology: "It gets easier every week!"
    data.append({
        'CyclesPerYear': 0,
        'Label': "Reverse 52-Week",
        'TotalSavings': w_total, # Same as normal 52-week (68900)
        'TotalCouple': w_total * 2,
        'MaxDailyAmount': 2600, # Hardest day is Day 1 (or Week 1)
        'AvgDaysPerCycle': 7,
        'Desc': "Start High, End Low"
    })
    
    # 5. Payday Sync (1st & 16th)
    # Psychology: "Sync with income, ignore other days"
    # 24 paydays * 3000 = 72000
    payday_amount = 3000
    payday_total = payday_amount * 24
    data.append({
        'CyclesPerYear': 0,
        'Label': "Payday Sync (1st&16th)",
        'TotalSavings': payday_total,
        'TotalCouple': payday_total * 2,
        'MaxDailyAmount': payday_amount, # High spike but rare
        'AvgDaysPerCycle': 15,
        'Desc': "3000฿ on Paydays Only"
    })
    
    # 6. No-Spend Weekends (Weekday Heavy)
    # Psychology: "Work hard M-F, play hard Sat-Sun"
    # 300 * 5 days = 1500/week -> 1500 * 52 = 78000
    weekday_amt = 300
    weekday_total = (weekday_amt * 5) * 52
    data.append({
        'CyclesPerYear': 0,
        'Label': "No-Spend Weekends",
        'TotalSavings': weekday_total,
        'TotalCouple': weekday_total * 2,
        'MaxDailyAmount': weekday_amt,
        'AvgDaysPerCycle': 0,
        'Desc': "M-F 300฿, Sat-Sun 0฿"
    })

    # 7. Aggressive Ladder (High Rollers)
    # Mon=100, Tue=200 ... Sun=700. (Sum=2800/week)
    agg_ladder_week = sum([100 * i for i in range(1, 8)]) # 2800
    agg_ladder_total = agg_ladder_week * 52 # 145600
    data.append({
        'CyclesPerYear': 0,
        'Label': "Aggressive Ladder",
        'TotalSavings': agg_ladder_total,
        'TotalCouple': agg_ladder_total * 2,
        'MaxDailyAmount': 700,
        'AvgDaysPerCycle': 0,
        'Desc': "Mon=100...Sun=700"
    })

    # 8. Coffee Skip (Micro-Habit)
    # 60 baht/day
    coffee_total = 60 * 365
    data.append({
        'CyclesPerYear': 0,
        'Label': "Coffee Skip (60฿)",
        'TotalSavings': coffee_total,
        'TotalCouple': coffee_total * 2,
        'MaxDailyAmount': 60,
        'AvgDaysPerCycle': 0,
        'Desc': "Skip 1 coffee/day"
    })

    # 9. Weekend Binge (Opposite of No-Spend)
    # M-F = 0. Sat=1000, Sun=1000.
    # 2000 * 52 = 104000
    binge_total = 2000 * 52
    data.append({
        'CyclesPerYear': 0,
        'Label': "Weekend Binge",
        'TotalSavings': binge_total,
        'TotalCouple': binge_total * 2,
        'MaxDailyAmount': 1000,
        'AvgDaysPerCycle': 0,
        'Desc': "M-F 0฿, Sat/Sun 1k"
    })
    
    # --- Round 3: New Variations ---
    
    # 10. Date Match (x10)
    # 1st = 10, 15th = 150, 31st = 310.
    # Approx calculation: 12 months * avg 30.4 days
    # Let's be precise: 7*31 + 4*30 + 1*28 (ignore leap for simple)
    # Sum 1..31 = 496. Sum 1..30 = 465. Sum 1..28 = 406.
    date_match_total = (496 * 7 + 465 * 4 + 406) * 10 # 57380
    data.append({
        'CyclesPerYear': 0,
        'Label': "Date Match (x10)",
        'TotalSavings': date_match_total,
        'TotalCouple': date_match_total * 2,
        'MaxDailyAmount': 310,
        'AvgDaysPerCycle': 30,
        'Desc': "Day 1=10฿ ... Day 31=310฿"
    })
    
    # 11. Odd/Even Smasher (Volatility)
    # Odd Day = 50, Even Day = 500.
    # 183 Odd days, 182 Even days.
    odd_even_total = (183 * 50) + (182 * 500) # 9150 + 91000 = 100150
    data.append({
        'CyclesPerYear': 0,
        'Label': "Odd/Even Smasher",
        'TotalSavings': odd_even_total,
        'TotalCouple': odd_even_total * 2,
        'MaxDailyAmount': 500,
        'AvgDaysPerCycle': 0,
        'Desc': "Odd=50฿, Even=500฿"
    })
    
    # 12. Workday Escalator (Beginner)
    # M=50, T=100, W=150, Th=200, F=250. Sat/Sun=0.
    # Sum = 750/week.
    escalator_total = 750 * 52 # 39000
    data.append({
        'CyclesPerYear': 0,
        'Label': "Workday Escalator",
        'TotalSavings': escalator_total,
        'TotalCouple': escalator_total * 2,
        'MaxDailyAmount': 250,
        'AvgDaysPerCycle': 0,
        'Desc': "M->F 50,100..250. Wknd 0"
    })

    df = pd.DataFrame(data)
    # SORTING: Sort by Total Savings (Highest first)
    return df.sort_values(by='TotalSavings', ascending=False)

def explain_strategies(df):
    print("\n" + "="*80)
    print(f"{'STRATEGY NAME':<25} | {'HOW IT WORKS (LOGIC)':<35} | {'YEARLY TOTAL (฿)':>15}")
    print("="*80)
    for index, row in df.iterrows():
        print(f"{row['Label']:<25} | {row['Desc']:<35} | {row['TotalSavings']:>15,.0f}")
    print("="*80 + "\n")

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # Focus on "interesting" human-readable cycles
    interesting_cycles = [1, 2, 4, 6, 12, 24, 26, 52, 365]
    df = generate_comparison_data(interesting_cycles, YEAR_DAYS)
    
    # Print the Explanation Table
    explain_strategies(df)
    
    # Find max
    best_config = df.iloc[0] # Since it's sorted
    
    print(f"--- Optimization Analysis ---")
    print(f"Winner: {best_config['Label']}")
    print(f"Max Savings Possible (1 Person): ฿{best_config['TotalSavings']:,.2f}")

    # Visualization
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Label'],
        y=df['TotalSavings'],
        # Color bars by how "painful" the max payment is
        marker=dict(
            color=df['MaxDailyAmount'],
            colorscale='RdYlGn_r', # Green (Easy) -> Yellow -> Red (Hard)
            cmin=0,     # Start Green at 0
            cmax=1000,  # Cap Red at 1000
            colorbar=dict(title="Max Daily Pay (฿)"),
            showscale=True
        ),
        name='Total Savings',
        # Updated Tooltip
        hovertemplate='<b>%{x}</b><br>' +
                      'Logic: %{customdata[4]}<br>' +
                      '<b>Max Daily Pay: ฿%{customdata[2]:,.0f}</b><br><br>' +
                      '1 Person: ฿%{y:,.2f}<br>' +
                      '2 People: ฿%{customdata[1]:,.2f}<extra></extra>',
        # Pass AvgDays, TotalCouple, MaxDailyAmount, CyclesPerYear, Desc
        customdata=df[['AvgDaysPerCycle', 'TotalCouple', 'MaxDailyAmount', 'CyclesPerYear', 'Desc']]
    ))

    fig.add_trace(go.Scatter(
        x=df['Label'],
        y=df['TotalSavings'],
        mode='text',
        text=df['TotalSavings'].apply(lambda x: f'฿{x:,.0f}'),
        textposition='top center',
        showlegend=False
    ))

    fig.update_layout(
        title='<b>Ranked Savings Strategies (Pitch Deck)</b><br>'
              '<sup><span style="color:green"><b>Green = Easy (<100฿)</b></span> → <span style="color:orange"><b>Orange</b></span> → <span style="color:red"><b>Red = Hard (>1000฿)</b></span></sup>',
        xaxis_title='Strategy',
        yaxis_title='Total Savings (฿)',
        template='plotly_white',
        hovermode='x unified'
    )

    # --- Pitch Deck Visuals ---
    
    # 1. The "Beat the Baseline" Line
    # User's original plan was Yearly (1) = ~66,795
    baseline_val = 66795
    fig.add_hline(
        y=baseline_val, 
        line_dash="dash", 
        line_color="black",
        annotation_text="<b>ORIGINAL PLAN (Yearly)</b>", 
        annotation_position="top right"
    )

    # 2. Highlight the "Sweet Spot" Winner
    # No-Spend Weekends (78k) is high return but easier than the 100k ones
    # Find its value
    winner_row = df[df['Label'] == "No-Spend Weekends"]
    if not winner_row.empty:
        fig.add_annotation(
            x="No-Spend Weekends",
            y=winner_row['TotalSavings'].values[0],
            text="🏆 Best Balance<br>(High Yield / Low Stress)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636efa",
            yshift=10
        )

    fig.show()
    print("\nComparison script completed.")
    
    # Limit number of X ticks to be readable
    # fig.update_xaxes(nticks=20)

    fig.show()
    print("\nComparison script completed.")
