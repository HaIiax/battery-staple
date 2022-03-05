import os

from queries import Queries


class RideSchedulePublisher:
    def __init__(self, event_date=None):
        self.event_date = event_date
        if self.event_date is None:
            self.event_date = Queries.getCurrentEventDate()
        with open(os.path.realpath(__file__).replace('.py', '.js')) as jsstring:
            self.js = jsstring.read()

    def asHTML(self):
        import makeHTML
        from queries import Queries

        page = makeHTML.part('html')

        head = None
        body = None
        # Query is sorted by time, location, model
        # model is the car model, driven by driver_name
        # rider_name is name of rider for a given time, model, location
        ptime = None
        pmodel = None
        plocation = None
        tab_count = 0
        time_count = 1  # 'All' as first time
        # select event_date, event_name, time, location, car_owner_name as driver_name, car_id, model, rider_name, user_id
        riders = Queries.getCurrentEventRide(self.event_date)
        for rider in riders:
            if head is None:
                title = rider['event_name'] + " on " + rider['event_date']
                head = page.addPart('head')
                head.addPart('meta', attributes={"charset": "utf-8"})
                head.addPart('meta', attributes={
                             "name": "viewport", "content": "width=device-width, initial-scale=1"})
                head.addPart('title', content=title)
                head.addPart('script', content=self.js)
                head.addPart('link', attributes={
                             "rel": "stylesheet", "href": "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"})

            if body is None:
                body = page.addPart('body')
                section = body.addPart(
                    'section', style="section")
                panel = section.addPart('nav', style="panel")
                panel.addPart(style="panel-heading has-text-centered", content=rider['event_name']).addPart(
                    'br').addPart('span', style='is-size-7', content=rider['event_date'])
                panel_tabs = panel.addPart(style="panel-tabs")
                time_nav = panel_tabs.addPart('a', style="nav-link pr-6 pl-6 is-active", content="Time",
                                              attributes={"data-target": "time-tabs|time-panel"})
                driver_nav = panel_tabs.addPart('a', style="nav-link pr-6 pl-6 ", content="Driver", attributes={
                    "data-target": "driver-tabs|driver-panel"})

                time_tabs = panel_tabs.addPart(
                    style="panel-tabs", id="time-tabs")
                time_tabs.addPart('a', style="time-link is-active",
                                  content='All', attributes={"data-target": "all"})

                driver_tabs = panel_tabs.addPart(
                    style="panel-tabs is-hidden", id="driver-tabs")
                driver_tabs.addPart('a', style="driver-link is-active",
                                    content='All', attributes={"data-target": "all"})

                time_panel = panel.addPart('span', id="time-panel")
                driver_panel = panel.addPart(
                    'span', style="is-hidden", id="driver-panel")

            time = rider['time']
            model = rider['model']
            seats = rider['seats']
            parking_spot = rider['parking_spot']
            driver_name = rider['driver_name']
            location = rider['location']
            rider_name = rider['rider_name']

            if ptime != time:
                if time_count % 4 == 0:
                    tab_count += 1
                    nav_id = "time-tabs-" + str(tab_count)
                    time_nav.attributes['data-target'] += '|' + nav_id
                    time_tabs = panel_tabs.addPart(
                        style="panel-tabs", id=nav_id)
                time_count += 1
                time_tabs.addPart('a', style="time-link",
                                  content=time, attributes={"data-target": time})
                time_div = time_panel.addPart(
                    'div', style="panel-block", id=time).addPart('div', style="columns")
                ptime = time
                pmodel = None
                plocation = None

            if plocation != location:
                plocation = location
                pmodel = None
                location_card = time_div.addPart('div', style="column").addPart(
                    'div', style="card has-background-grey has-text-light")
                location_card.addPart('header', style="card-header").addPart(
                    style="card-header-title has-background-light", content=location + " @" + time)

            if pmodel != model:
                pmodel = model
                content = location_card.addPart('div',
                                                style="card-content has-text-centered",
                                                content=model).addPart('div', style="is-size-7 has-text-centered", content="Driver: " + driver_name).addPart('div',
                                                                                                                                                             style="is-size-7 has-text-centered", content=seats + " seats @" + parking_spot).addPart('div')

            content.addPart('span', style="tag", content=rider_name)

        # Add to the driver_panel
        riders.sort(key=lambda r: r['driver_name'] + '/' +
                    r['time'] + '/' + r['location'] + '/' + r['rider_name'])
        ptime = None
        pmodel = None
        plocation = None
        driver_count = 1  # 'All' is added as first driver
        tab_count = 0
        for rider in riders:
            time = rider['time']
            model = rider['model']
            seats = rider['seats']
            parking_spot = rider['parking_spot']
            driver_name = rider['driver_name']
            location = rider['location']
            rider_name = rider['rider_name']

            if pmodel != model:
                if driver_count % 4 == 0:
                    tab_count += 1
                    nav_id = "driver-tabs-" + str(tab_count)
                    driver_nav.attributes['data-target'] += '|' + nav_id
                    driver_tabs = panel_tabs.addPart(
                        style="panel-tabs is-hidden", id=nav_id)
                driver_count += 1
                pmodel = model
                ptime = None
                plocation = None
                driver_tabs.addPart('a', style="driver-link",
                                    content=driver_name, attributes={"data-target": driver_name})
                driver_div = driver_panel.addPart(
                    'div', style="panel-block", id=driver_name).addPart('div', style="columns")
                driver_card = driver_div.addPart('div', style="column").addPart(
                    'div', style="card has-background-grey has-text-light")
                driver_card.addPart('header', style="card-header").addPart(
                    style="card-header-title has-background-light", content=driver_name + " (" + model + ", " + seats + " seats @" + parking_spot + ")")

            if ptime != time:
                ptime = time
                plocation = None
                time_content = driver_card.addPart(
                    'div', style="card-content", content=time)

            if plocation != location:
                plocation = location
                location_content = time_content.addPart(
                    'div', style="card-content", content=location)

            location_content.addPart('span', style="tag", content=rider_name)

        return '<!DOCTYPE html>\n' + page.make()
