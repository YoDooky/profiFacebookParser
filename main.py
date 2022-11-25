import json
from typing import TypedDict
from typing import Dict, List
from save_to_excel import ExcelData


class FBData(TypedDict):
    card_data: str
    facebook_url: str


class CollectData:
    def __init__(self, src: Dict):
        self.card_data = src.get('card_data')
        self.facebook_url = src.get('facebook_url')

    def get_group_name(self) -> str:
        """Get group name"""
        delimeter = '\n'
        group_title = self.card_data.split(delimeter)[0]
        self.card_data = self.card_data.replace(f'{group_title}{delimeter}', '')
        return group_title

    def get_group_facebook_link(self) -> str:
        """Get link to facebook"""
        return self.facebook_url

    def get_group_type(self) -> str:
        """Opened or private"""
        delimeter = ' · '
        group_type = self.card_data.split(delimeter)[0]
        self.card_data = self.card_data.replace(f'{group_type}{delimeter}', '')
        return group_type

    def get_group_members_amount(self) -> str:
        """Get amount of group members"""
        delimeter = ' · '
        members_amount = self.card_data.split(delimeter)[0].split('Участники: ')[1]
        self.card_data = self.card_data.replace(f'Участники: {members_amount}{delimeter}', '')
        return members_amount

    def get_group_post_rate(self) -> str:
        """Get group posts amount per day"""
        delimeter = '\n'
        post_rate = self.card_data.split(delimeter)[0]
        self.card_data = self.card_data.replace(f'{post_rate}{delimeter}', '')
        return post_rate

    def get_group_websites(self) -> str:
        """Get group websites"""
        delimeter = ['http', ' www.']
        target_string = self.card_data
        url_list = []
        for delimeter in delimeter:
            target_index = target_string.find(delimeter)
            if target_index < 0:
                continue
            web_pages = target_string.split(delimeter)
            url_list = [*url_list, *[f'{delimeter}{page.split(" ")[0]}' for page in web_pages[1::]]]
        return ', '.join(url_list)

    def get_group_about(self) -> str:
        """Get group about info"""
        delimeter = '\n'
        about_info = self.card_data.split(delimeter)[0]
        self.card_data = self.card_data.replace(f'{about_info}{delimeter}', '')
        return about_info

    def get_card_info(self) -> Dict:
        """Collects all group info"""
        return {
            'title': self.get_group_name(),
            'facebook_link': self.get_group_facebook_link(),
            'type': self.get_group_type(),
            'members_amount': self.get_group_members_amount(),
            'post_rate': self.get_group_post_rate(),
            'websites': self.get_group_websites(),
            'about': self.get_group_about()
        }


def get_json(file_name: str) -> List[Dict]:
    with open(f'json/{file_name}.json', 'r', encoding='utf-8') as file:
        src = json.loads(file.read())
    return src


def save_json(file_src: List[Dict], file_name: str):
    with open(f'json/{file_name}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(file_src))


def get_data_from_json(filename):
    filename = 'asic_mining'
    json_data = get_json(filename)
    group_info = []
    for data in json_data:
        collect_data = CollectData(data)
        group_info.append(collect_data.get_card_info())
    save_json(group_info, f'{filename}_complete')


def main():
    filename = 'crypto_mining'
    # get_page_src.get_webpage_data()
    # get_data_from_json(filename)
    excel_data = ExcelData(f'{filename}_complete')
    excel_data.write_data_to_excel()


if __name__ == '__main__':
    main()
