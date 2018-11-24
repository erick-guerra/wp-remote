import requests
from texttable import Texttable

#TODO: create texttable for fetch_info()
#TODO: Create a 'mass pass' of arguments to create multiple wp=remotes at the same time
#TODO: 'Mass-pass' must be able to then store site info with its api
#TODO: Figure out how the WPremote plugin store the API on wpsite for insertion
#TODO: figure a way to activate pluggins in 'bulk'
#TODO: Clean up CODE!!

class WpRemote(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.end_point = 'https://wpremote.com/api/json/site'
        self.sites = {}
        self.site_select = ''
        self.site_select_id = ''
        self.site_select_name = ''
        self.site_select_json = ''

    def fetch_info(self):
        table = Texttable()
        res = requests.get(self.end_point, auth=(self.api_key, ''))
        res_len = len(res.json())
        table.add_row(['SITE #', 'DETAILS'])
        for x in range(res_len):
            # print(req.json()[x].keys())
            nicename = res.json()[x]['nicename']
            remote_id = res.json()[x]['ID']
            plugin_api_key = res.json()[x]['api_key']
            company_id = res.json()[x]['company_id']
            table.add_row([x, [['Remote Name', nicename, 'WP SITE ID', remote_id, 'WPREMOTE API', plugin_api_key]]])
            self.sites[str(x)] = {'Site_Title': nicename, 'ID': remote_id,
                                  'Plugin_Api': plugin_api_key, 'company_id': company_id}
            #print('Nice name: {}\nID: {}\nSite api key: {}'.format(nicename, remote_id, plugin_api_key))
        print(table.draw())

    def set_site(self, site):
        self.site_select = self.sites.get(site)
        self.site_select_id = self.site_select['ID']
        self.site_select_name = self.site_select['Site_Title']
        return self.sites.get(site)

    def get_site_info(self):
        site_res = requests.get(self.end_point + '/' + str(self.site_select_id), auth=(api_key, ''))
        return site_res.json()

    def set_site_select(self):
        self.site_select_json = self.get_site_info()

    def parse_site_info(self):
        table = Texttable()
        nice_name = self.site_select_json['nicename']
        site_url = self.site_select_json['url']
        site_id = self.site_select_json['ID']
        company_id = self.site_select_json['company_id']
        site_api_key = self.site_select_json['api_key']
        update_status = self.site_select_json['can_update']
        # Iterable
        site_sumup = self.site_select_json['site_summary'].items()
        status = self.site_select_json['status_message']
        themes = self.site_select_json['themes']
        plugins = self.site_select_json['plugins']
        #site_notes = self.site_select_json['site_note']
        table.add_rows([['SITE INFO', 'DETAILS'],
                        ['NiceName', nice_name],
                        ['Site Url', site_url],
                        ['Site ID', site_id],
                        ['Site API', site_api_key],
                        ['Can update', update_status],
                        ['Status Message', status]])
        print(table.draw())
        # print("SITES INFO:\n")
        # print('SITE: {}\nSITE URL: {}\nSITE ID: {}\nAPI: {}\nCAN UPDATE: {}\n'.format(nice_name, site_url,
        #                                                                             site_id, site_api_key,
        #                                                                             update_status))
        sum_table = Texttable()
        sum_table.add_row(['Site Detail', '# of'])
        print("Site Summary:\n")
        for k, v in site_sumup:
            sum_table.add_row([k, v])
            print(k, v)
        print(sum_table.draw())

        theme_table = Texttable()
        theme_table.add_row(['Theme '])
        for x in range(len(themes)):
            theme_table = Texttable()
            theme_name = self.site_select_json['themes'][x]['name']
            theme_slug = self.site_select_json['themes'][x]['slug']
            theme_version = self.site_select_json['themes'][x]['version']
            theme_latest_version = self.site_select_json['themes'][x]['latest_version']
            active_status = self.site_select_json['themes'][x]['is_active']
            theme_table.add_rows([['Theme', theme_name], ['Slug', theme_slug], ['Current Version', theme_version],
                                  ['Theme latest Verion', theme_latest_version], ['Theme active', active_status]])
            print(theme_table.draw())
            print('Theme: {}\nSlug: {}\nVersion: {}\nActive? {}'.format(theme_name, theme_slug, theme_version,
                                                                        active_status))

        for plugin in range(len(plugins)):
            plugin_table = Texttable()
            plugin_name = self.site_select_json['plugins'][plugin]['name']
            plugin_slug = self.site_select_json['plugins'][plugin]['slug']
            plugin_version = self.site_select_json['plugins'][plugin]['version']
            plugin_lates_version = self.site_select_json['plugins'][plugin]['latest_version']
            active_status = self.site_select_json['plugins'][plugin]['is_active']
            plugin_table.add_rows([['Plugin', plugin_name], ['Slug', plugin_slug], ['Version', plugin_version],
                                   ['Plugin latest version', plugin_lates_version], ['Is active', active_status]])
            print(plugin_table.draw())
            print('Plugin Name: {}\nSlug: {}\nVersion: {}\nLatest Version:{}\nActive? {}\n'.format(plugin_name,
                                                                                                 plugin_slug,
                                                                                                 plugin_version,
                                                                                                 plugin_lates_version,
                                                                                                 active_status))

    def delete_site(self):
        print("The current site selected is: {} | ID: {}".format(self.site_select_name, self.site_select_id))
        ask = input("Are you sure you want to delete? (y/n)\n")
        if 'y' or 'Y' in ask:
            del_req = requests.delete(self.end_point + '/' + str(self.site_select_id), auth=(api_key, ''))
        self.fetch_info()

    def post_site(self):
        domain = str(input("Enter New Domain Name:\n"))
        company_id = str(input("Enter Company ID: (Default= 2 (SPN))"))
        if company_id == '':
            company_id = '2'
        nicename = str(input("What nice name shall we give it?\n"))
        #group (check docs for extendification)
        params = {'domain': domain, 'company_id': company_id, 'nicename': nicename}
        requests.post(self.end_point, auth=(api_key, ''), data=params)












        # self.site_select_json['lock_core_status']
        # self.site_select_json['lock_site_status']
        # self.site_select_json['remote_log_enabled']
        # self.site_select_json['version_status']
        # self.site_select_json['favicon']
        # self.site_select_json['supported_filesystem_methods']
        # self.site_select_json['company_name']
        # self.site_select_json['next_automatic_backup_date']
        # self.site_select_json['home_url']
        # self.site_select_json['admin_path']
        # self.site_select_json['status_code']
        # self.site_select_json['is_refreshing']
        # self.site_select_json['upgrade_url']
        # self.site_select_json['last_refresh_verbose']
        # self.site_select_json['is_premium']
        # self.site_select_json['filesystem_method']
        # self.site_select_json['has_wpremote_plugin']
        # self.site_select_json['backups']
        # self.site_select_json['version']
        # self.site_select_json['latest_version']
        # self.site_select_json['http_auth_username']
        # self.site_select_json['automatic_core_updates_enabled']
        # self.site_select_json['email_frequency']
        # self.site_select_json['response']
        # self.site_select_json['automatic_theme_updates_enabled']
        # self.site_select_json['admin_url']
        # self.site_select_json['automatic_plugin_updates_enabled']
        # self.site_select_json['site_url']
        # self.site_select_json['last_refresh']
        # self.site_select_json['group']