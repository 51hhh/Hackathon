from flask import Blueprint, jsonify, request
import json
import calendar
from datetime import datetime, date

calendar_bp = Blueprint('calendar_api', __name__)

@calendar_bp.route('/calendar_data')
def get_calendar_data():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not year or not month:
        today = date.today()
        year = today.year
        month = today.month

    cal = calendar.Calendar(firstweekday=6) # Sunday as the first day of the week
    month_days = cal.monthdayscalendar(year, month)

    calendar_days = []
    today_date = date.today()

    with open('data/interactions.json', 'r', encoding='utf-8') as f:
        all_interactions = json.load(f)

    for week in month_days:
        for day_num in week:
            is_current_month = True
            if day_num == 0: # Days from previous/next month
                is_current_month = False
                day_number_display = ''
            else:
                day_number_display = day_num

            current_day_date = None
            if is_current_month:
                try:
                    current_day_date = date(year, month, day_num)
                except ValueError:
                    current_day_date = None

            is_today = (current_day_date == today_date) if current_day_date else False
            
            # Get interactions for the current day
            interactions_key = f"{year}-{month:02d}-{day_num:02d}"
            interactions = all_interactions.get(interactions_key, [])

            calendar_days.append({
                'day_number': day_number_display,
                'is_current_month': is_current_month,
                'is_today': is_today,
                'interactions': interactions
            })

    current_month_name = datetime(year, month, 1).strftime('%B')

    return jsonify({
        'current_month_name': current_month_name,
        'current_year': year,
        'calendar_days': calendar_days
    })
