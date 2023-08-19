from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mypass.db.db import db
from mypass.models.user import User
from mypass.models.entry import VaultEntry, Tag


def insert_data(session, *objs):
    for obj in objs:
        session.add(obj)
    session.commit()


def print_all(objs):
    for obj in objs:
        print(obj)


def main():
    engine = create_engine('sqlite://')
    db.metadata.create_all(engine)

    with Session(bind=engine) as session:
        user1 = User.create(username='test1', password='pdw123')
        user2 = User.create(username='test2', password='pdw123')

        vault_entry1 = VaultEntry(user_id=1, username='uname', password='123', salt='pepper', website='Facebook')
        vault_entry2 = VaultEntry(user_id=1, username='uname', password='123', salt='pepper', website='GitHub')

        tag0 = Tag(user_id=1, name='Important')

        tag1 = Tag(user_id=1, name='Social')
        tag2 = Tag(user_id=1, name='Personal')

        tag3 = Tag(user_id=1, name='Work')
        tag4 = Tag(user_id=1, name='Development')

        vault_entry1.tags.append(tag0)
        vault_entry2.tags.append(tag0)

        vault_entry1.tags.append(tag1)
        vault_entry1.tags.append(tag2)

        vault_entry2.tags.append(tag3)
        vault_entry2.tags.append(tag4)

        insert_data(session, user1, user2, vault_entry1, vault_entry2)

        users = session.query(User)
        vault_entries = session.query(VaultEntry)
        tags = session.query(Tag)

        print('\nListing:')
        print('------------')
        print('All user:')
        print_all(users)
        print('\nAll vault entry:')
        print_all(vault_entries)
        print('\nAll tag:')
        print_all(tags)

        print('\nUser id=1:')
        print('------------')
        print('User id=1 vault_entries')
        print_all(users[0].vault_entries)

        print('\nUser id=1 tags')
        print_all(users[0].tags)

        print('\nUser id=1 vault_entries[0].tags')
        print_all(users[0].vault_entries[0].tags)

        print('\nUser id=1 tags[0].vault_entries')
        print_all(users[0].tags[0].vault_entries)


if __name__ == '__main__':
    main()
