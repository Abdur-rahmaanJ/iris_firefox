# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case perform 2 selections at the same time.',
        locale=['en-US'],
        test_case_id='108257',
        test_suite_id='1902',
    )
    def run(self, firefox):

        hover_duck_duck_go_one_off_button_pattern = Pattern('hover_duck_duck_go_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        search_with_url_autocomplete_pattern = Pattern('search_with_url_autocomplete.png')
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png')
        default_status_pattern = Pattern('default_status.png')
        modified_status_pattern = Pattern('modified_status.png')
        true_value_pattern = Pattern('true_value.png')
        false_value_pattern = Pattern('false_value.png')
        amazon_logo_pattern = Pattern('amazon_logo.png')
        accept_risk_pattern = Pattern('accept_risk.png')

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate('www.amazon.com')

        expected = exists(amazon_logo_pattern, 10)
        assert expected, 'Page successfully loaded, amazon logo found.'

        navigate('about:config')

        # Change focus from the url bar.
        if OSHelper.is_windows() or OSHelper.is_linux():
            click(NavBar.HAMBURGER_MENU.target_offset(-170, 15))
            type(Key.ENTER)
        else:
            if exists(accept_risk_pattern):
                click(accept_risk_pattern)
        expected = region.exists(default_status_pattern, 10)
        assert expected, 'The \'about:config\' page successfully loaded and default status is correct.'

        paste('keyword.enabled')
        type(Key.ENTER)

        expected = region.exists(default_status_pattern, 10)
        assert expected, 'The \'keyword.enabled\' preference has status \'default\' by default.'

        expected = region.exists(true_value_pattern, 10)
        assert expected, 'The \'keyword.enabled\' preference has value \'true\' by default.'

        double_click(default_status_pattern)

        expected = region.exists(modified_status_pattern, 10)
        assert expected, 'The \'keyword.enabled\' preference has status \'modified\' after the preference has changed.'

        expected = region.exists(false_value_pattern, 10)
        assert expected, 'The \'keyword.enabled\' preference has value \'false\' after the preference has changed.'

        select_location_bar()
        paste('amaz')

        expected = region.exists(search_with_url_autocomplete_pattern, 10)
        assert expected, 'Search is performed with url autocomplete for pages where you have been before.'

        hover(duck_duck_go_one_off_button_pattern)

        expected = exists(hover_duck_duck_go_one_off_button_pattern, 10)
        assert expected, 'Mouse is over the \'DuckDuckGo\' search engine.'

        expected = region.exists(search_with_url_autocomplete_pattern, 10)
        assert expected, 'The autocomplete is still displayed after user hovers an one-off button.'

        repeat_key_up(3)
        key_to_one_off_search(twitter_one_off_button_highlight_pattern)

        expected = region.exists(twitter_one_off_button_highlight_pattern, 10)
        assert expected, 'The \'Twitter\' one-off button is highlighted.'
