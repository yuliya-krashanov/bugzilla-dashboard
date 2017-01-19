# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, SmallInteger, String, Table, text
from sqlalchemy.dialects.mysql.base import LONGBLOB
from sqlalchemy.orm import relationship
from dashboard.database import BugzillaBase as Base

metadata = Base.metadata


class Attachment(Base):
    __tablename__ = 'attachments'
    __table_args__ = (
        Index('attachments_submitter_id_idx', 'submitter_id', 'bug_id'),
    )

    attach_id = Column(Integer, primary_key=True)
    bug_id = Column(ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    creation_ts = Column(DateTime, nullable=False, index=True)
    description = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    ispatch = Column(Integer, nullable=False, server_default=text("'0'"))
    filename = Column(String(255), nullable=False)
    submitter_id = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False)
    isobsolete = Column(Integer, nullable=False, server_default=text("'0'"))
    isprivate = Column(Integer, nullable=False, server_default=text("'0'"))
    modification_time = Column(DateTime, nullable=False, index=True)

    bug = relationship(u'Bug')
    submitter = relationship(u'Profile')


class AttachDatum(Attachment):
    __tablename__ = 'attach_data'

    id = Column(ForeignKey(u'attachments.attach_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True)
    thedata = Column(LONGBLOB, nullable=False)


t_audit_log = Table(
    'audit_log', metadata,
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'SET NULL', onupdate=u'CASCADE'), index=True),
    Column('class', String(255), nullable=False),
    Column('object_id', Integer, nullable=False),
    Column('field', String(64), nullable=False),
    Column('removed', String),
    Column('added', String),
    Column('at_time', DateTime, nullable=False),
    Index('audit_log_class_idx', 'class', 'at_time')
)


t_bug_group_map = Table(
    'bug_group_map', metadata,
    Column('bug_id', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('group_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('bug_group_map_bug_id_idx', 'bug_id', 'group_id', unique=True)
)


class BugSeeAlso(Base):
    __tablename__ = 'bug_see_also'
    __table_args__ = (
        Index('bug_see_also_bug_id_idx', 'bug_id', 'value', unique=True),
    )

    id = Column(Integer, primary_key=True)
    bug_id = Column(ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    value = Column(String(255), nullable=False)
    _class = Column('class', String(255), nullable=False, server_default=text("''"))

    bug = relationship(u'Bug')


class BugSeverity(Base):
    __tablename__ = 'bug_severity'
    __table_args__ = (
        Index('bug_severity_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class BugStatu(Base):
    __tablename__ = 'bug_status'
    __table_args__ = (
        Index('bug_status_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    is_open = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


t_bug_tag = Table(
    'bug_tag', metadata,
    Column('bug_id', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('tag_id', ForeignKey(u'tag.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('bug_tag_bug_id_idx', 'bug_id', 'tag_id', unique=True)
)


class Bug(Base):
    __tablename__ = 'bugs'

    bug_id = Column(Integer, primary_key=True)
    assigned_to = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    bug_file_loc = Column(String, nullable=False)
    bug_severity = Column(String(64), nullable=False, index=True)
    bug_status = Column(String(64), nullable=False, index=True)
    creation_ts = Column(DateTime, index=True)
    delta_ts = Column(DateTime, nullable=False, index=True)
    short_desc = Column(String(255), nullable=False)
    op_sys = Column(String(64), nullable=False, index=True)
    priority = Column(String(64), nullable=False, index=True)
    product_id = Column(ForeignKey(u'products.id', onupdate=u'CASCADE'), nullable=False, index=True)
    rep_platform = Column(String(64), nullable=False)
    reporter = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    version = Column(String(64), nullable=False, index=True)
    component_id = Column(ForeignKey(u'components.id', onupdate=u'CASCADE'), nullable=False, index=True)
    resolution = Column(String(64), nullable=False, index=True, server_default=text("''"))
    target_milestone = Column(String(64), nullable=False, index=True, server_default=text("'---'"))
    qa_contact = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), index=True)
    status_whiteboard = Column(String, nullable=False)
    votes = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    lastdiffed = Column(DateTime)
    everconfirmed = Column(Integer, nullable=False)
    reporter_accessible = Column(Integer, nullable=False, server_default=text("'1'"))
    cclist_accessible = Column(Integer, nullable=False, server_default=text("'1'"))
    estimated_time = Column(Numeric(7, 2), nullable=False, server_default=text("'0.00'"))
    remaining_time = Column(Numeric(7, 2), nullable=False, server_default=text("'0.00'"))
    alias = Column(String(20), unique=True)
    deadline = Column(DateTime)
    # cf_browser = Column(String(64), nullable=False, server_default=text("'---'"))
    # cf_revision = Column(String(255), nullable=False, server_default=text("''"))
    # cf_testingplanitems = Column(String(255), nullable=False, server_default=text("''"))
    # cf_ext_tracker_status = Column(String(64), nullable=False, server_default=text("'---'"))
    # cf_label = Column(String(255), nullable=False, server_default=text("''"))

    profile = relationship(u'Profile', primaryjoin='Bug.assigned_to == Profile.userid')
    component = relationship(u'Component')
    product = relationship(u'Product')
    profile1 = relationship(u'Profile', primaryjoin='Bug.qa_contact == Profile.userid')
    profile2 = relationship(u'Profile', primaryjoin='Bug.reporter == Profile.userid')
    groups = relationship(u'Group', secondary='bug_group_map')
    profiles = relationship(u'Profile', secondary='cc')
    tags = relationship(u'Tag', secondary='bug_tag')
    keyworddefs = relationship(u'Keyworddef', secondary='keywords')
    parents = relationship(
        u'Bug',
        secondary='duplicates',
        primaryjoin=u'Bug.bug_id == duplicates.c.dupe',
        secondaryjoin=u'Bug.bug_id == duplicates.c.dupe_of'
    )
    parents1 = relationship(
        u'Bug',
        secondary='dependencies',
        primaryjoin=u'Bug.bug_id == dependencies.c.blocked',
        secondaryjoin=u'Bug.bug_id == dependencies.c.dependson'
    )


class BugsActivity(Base):
    __tablename__ = 'bugs_activity'

    bug_id = Column(ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    attach_id = Column(ForeignKey(u'attachments.attach_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    who = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    bug_when = Column(DateTime, nullable=False, index=True)
    fieldid = Column(ForeignKey(u'fielddefs.id', onupdate=u'CASCADE'), nullable=False, index=True)
    added = Column(String(255), index=True)
    removed = Column(String(255), index=True)
    comment_id = Column(ForeignKey(u'longdescs.comment_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    id = Column(Integer, primary_key=True)

    attach = relationship(u'Attachment')
    bug = relationship(u'Bug')
    comment = relationship(u'Longdesc')
    fielddef = relationship(u'Fielddef')
    profile = relationship(u'Profile')


class BugsFulltext(Base):
    __tablename__ = 'bugs_fulltext'

    bug_id = Column(Integer, primary_key=True)
    short_desc = Column(String(255), nullable=False, index=True)
    comments = Column(String, index=True)
    comments_noprivate = Column(String, index=True)


t_bz_schema = Table(
    'bz_schema', metadata,
    Column('schema_data', LONGBLOB, nullable=False),
    Column('version', Numeric(3, 2), nullable=False)
)


t_category_group_map = Table(
    'category_group_map', metadata,
    Column('category_id', ForeignKey(u'series_categories.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('group_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('category_group_map_category_id_idx', 'category_id', 'group_id', unique=True)
)


t_cc = Table(
    'cc', metadata,
    Column('bug_id', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('who', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('cc_bug_id_idx', 'bug_id', 'who', unique=True)
)


class CfBrowser(Base):
    __tablename__ = 'cf_browser'
    __table_args__ = (
        Index('cf_browser_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class CfExtTrackerStatu(Base):
    __tablename__ = 'cf_ext_tracker_status'
    __table_args__ = (
        Index('cf_ext_tracker_status_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class Classification(Base):
    __tablename__ = 'classifications'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))


t_component_cc = Table(
    'component_cc', metadata,
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('component_id', ForeignKey(u'components.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Index('component_cc_user_id_idx', 'component_id', 'user_id', unique=True)
)


class Component(Base):
    __tablename__ = 'components'
    __table_args__ = (
        Index('components_product_id_idx', 'product_id', 'name', unique=True),
    )

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    product_id = Column(ForeignKey(u'products.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    initialowner = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    initialqacontact = Column(ForeignKey(u'profiles.userid', ondelete=u'SET NULL', onupdate=u'CASCADE'), index=True)
    description = Column(String, nullable=False)
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))

    profile = relationship(u'Profile', primaryjoin='Component.initialowner == Profile.userid')
    profile1 = relationship(u'Profile', primaryjoin='Component.initialqacontact == Profile.userid')
    product = relationship(u'Product')
    users = relationship(u'Profile', secondary='component_cc')


t_dependencies = Table(
    'dependencies', metadata,
    Column('blocked', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('dependson', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('dependencies_blocked_idx', 'blocked', 'dependson', unique=True)
)


t_duplicates = Table(
    'duplicates', metadata,
    Column('dupe_of', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('dupe', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True)
)


t_email_setting = Table(
    'email_setting', metadata,
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('relationship', Integer, nullable=False),
    Column('event', Integer, nullable=False),
    Index('email_setting_user_id_idx', 'user_id', 'relationship', 'event', unique=True)
)


t_field_visibility = Table(
    'field_visibility', metadata,
    Column('field_id', ForeignKey(u'fielddefs.id', ondelete=u'CASCADE', onupdate=u'CASCADE')),
    Column('value_id', SmallInteger, nullable=False),
    Index('field_visibility_field_id_idx', 'field_id', 'value_id', unique=True)
)


class Fielddef(Base):
    __tablename__ = 'fielddefs'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String, nullable=False)
    mailhead = Column(Integer, nullable=False, server_default=text("'0'"))
    sortkey = Column(SmallInteger, nullable=False, index=True)
    obsolete = Column(Integer, nullable=False, server_default=text("'0'"))
    type = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    custom = Column(Integer, nullable=False, server_default=text("'0'"))
    enter_bug = Column(Integer, nullable=False, server_default=text("'0'"))
    visibility_field_id = Column(ForeignKey(u'fielddefs.id', onupdate=u'CASCADE'), index=True)
    value_field_id = Column(ForeignKey(u'fielddefs.id', onupdate=u'CASCADE'), index=True)
    buglist = Column(Integer, nullable=False, server_default=text("'0'"))
    reverse_desc = Column(String)
    is_mandatory = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    is_numeric = Column(Integer, nullable=False, server_default=text("'0'"))
    long_desc = Column(String(255), nullable=False, server_default=text("''"))

    value_field = relationship(u'Fielddef', remote_side=[id], primaryjoin='Fielddef.value_field_id == Fielddef.id')
    visibility_field = relationship(u'Fielddef', remote_side=[id], primaryjoin='Fielddef.visibility_field_id == Fielddef.id')


t_flagexclusions = Table(
    'flagexclusions', metadata,
    Column('type_id', ForeignKey(u'flagtypes.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('product_id', ForeignKey(u'products.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True),
    Column('component_id', ForeignKey(u'components.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True),
    Index('flagexclusions_type_id_idx', 'type_id', 'product_id', 'component_id', unique=True)
)


t_flaginclusions = Table(
    'flaginclusions', metadata,
    Column('type_id', ForeignKey(u'flagtypes.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('product_id', ForeignKey(u'products.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True),
    Column('component_id', ForeignKey(u'components.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True),
    Index('flaginclusions_type_id_idx', 'type_id', 'product_id', 'component_id', unique=True)
)


class Flag(Base):
    __tablename__ = 'flags'
    __table_args__ = (
        Index('flags_bug_id_idx', 'bug_id', 'attach_id'),
    )

    id = Column(Integer, primary_key=True)
    type_id = Column(ForeignKey(u'flagtypes.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    status = Column(String(1), nullable=False)
    bug_id = Column(ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    attach_id = Column(ForeignKey(u'attachments.attach_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    creation_date = Column(DateTime, nullable=False)
    modification_date = Column(DateTime)
    setter_id = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    requestee_id = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), index=True)

    attach = relationship(u'Attachment')
    bug = relationship(u'Bug')
    requestee = relationship(u'Profile', primaryjoin='Flag.requestee_id == Profile.userid')
    setter = relationship(u'Profile', primaryjoin='Flag.setter_id == Profile.userid')
    type = relationship(u'Flagtype')


class Flagtype(Base):
    __tablename__ = 'flagtypes'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    cc_list = Column(String(200))
    target_type = Column(String(1), nullable=False, server_default=text("'b'"))
    is_active = Column(Integer, nullable=False, server_default=text("'1'"))
    is_requestable = Column(Integer, nullable=False, server_default=text("'0'"))
    is_requesteeble = Column(Integer, nullable=False, server_default=text("'0'"))
    is_multiplicable = Column(Integer, nullable=False, server_default=text("'0'"))
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    grant_group_id = Column(ForeignKey(u'groups.id', ondelete=u'SET NULL', onupdate=u'CASCADE'), index=True)
    request_group_id = Column(ForeignKey(u'groups.id', ondelete=u'SET NULL', onupdate=u'CASCADE'), index=True)

    grant_group = relationship(u'Group', primaryjoin='Flagtype.grant_group_id == Group.id')
    request_group = relationship(u'Group', primaryjoin='Flagtype.request_group_id == Group.id')


t_group_control_map = Table(
    'group_control_map', metadata,
    Column('group_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('product_id', ForeignKey(u'products.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('entry', Integer, nullable=False, server_default=text("'0'")),
    Column('membercontrol', Integer, nullable=False, server_default=text("'0'")),
    Column('othercontrol', Integer, nullable=False, server_default=text("'0'")),
    Column('canedit', Integer, nullable=False, server_default=text("'0'")),
    Column('editcomponents', Integer, nullable=False, server_default=text("'0'")),
    Column('editbugs', Integer, nullable=False, server_default=text("'0'")),
    Column('canconfirm', Integer, nullable=False, server_default=text("'0'")),
    Index('group_control_map_product_id_idx', 'product_id', 'group_id', unique=True)
)


t_group_group_map = Table(
    'group_group_map', metadata,
    Column('member_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('grantor_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('grant_type', Integer, nullable=False, server_default=text("'0'")),
    Index('group_group_map_member_id_idx', 'member_id', 'grantor_id', 'grant_type', unique=True)
)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String, nullable=False)
    isbuggroup = Column(Integer, nullable=False)
    userregexp = Column(String, nullable=False)
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    icon_url = Column(String)

    namedquerys = relationship(u'Namedquery', secondary='namedquery_group_map')


class Keyworddef(Base):
    __tablename__ = 'keyworddefs'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String, nullable=False)


t_keywords = Table(
    'keywords', metadata,
    Column('bug_id', ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('keywordid', ForeignKey(u'keyworddefs.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('keywords_bug_id_idx', 'bug_id', 'keywordid', unique=True)
)


t_login_failure = Table(
    'login_failure', metadata,
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('login_time', DateTime, nullable=False),
    Column('ip_addr', String(40), nullable=False)
)


class Logincooky(Base):
    __tablename__ = 'logincookies'

    cookie = Column(String(16), primary_key=True)
    userid = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    ipaddr = Column(String(40))
    lastused = Column(DateTime, nullable=False, index=True)

    profile = relationship(u'Profile')


class Longdesc(Base):
    __tablename__ = 'longdescs'
    __table_args__ = (
        Index('longdescs_who_idx', 'who', 'bug_id'),
        Index('longdescs_bug_id_idx', 'bug_id', 'work_time')
    )

    bug_id = Column(ForeignKey(u'bugs.bug_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    who = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    bug_when = Column(DateTime, nullable=False, index=True)
    work_time = Column(Numeric(7, 2), nullable=False, server_default=text("'0.00'"))
    thetext = Column(String, nullable=False)
    isprivate = Column(Integer, nullable=False, server_default=text("'0'"))
    already_wrapped = Column(Integer, nullable=False, server_default=text("'0'"))
    comment_id = Column(Integer, primary_key=True)
    type = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    extra_data = Column(String(255))

    bug = relationship(u'Bug')
    profile = relationship(u'Profile')


class Milestone(Base):
    __tablename__ = 'milestones'
    __table_args__ = (
        Index('milestones_product_id_idx', 'product_id', 'value', unique=True),
    )

    product_id = Column(ForeignKey(u'products.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    value = Column(String(64), nullable=False)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    id = Column(Integer, primary_key=True)
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))

    product = relationship(u'Product')


class Namedquery(Base):
    __tablename__ = 'namedqueries'
    __table_args__ = (
        Index('namedqueries_userid_idx', 'userid', 'name', unique=True),
    )

    userid = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    name = Column(String(64), nullable=False)
    query = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)

    profile = relationship(u'Profile')
    users = relationship(u'Profile', secondary='namedqueries_link_in_footer')


t_namedqueries_link_in_footer = Table(
    'namedqueries_link_in_footer', metadata,
    Column('namedquery_id', ForeignKey(u'namedqueries.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('namedqueries_link_in_footer_id_idx', 'namedquery_id', 'user_id', unique=True)
)


t_namedquery_group_map = Table(
    'namedquery_group_map', metadata,
    Column('namedquery_id', ForeignKey(u'namedqueries.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, unique=True),
    Column('group_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
)


class OpSy(Base):
    __tablename__ = 'op_sys'
    __table_args__ = (
        Index('op_sys_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class Priority(Base):
    __tablename__ = 'priority'
    __table_args__ = (
        Index('priority_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class Product(Base):
    __tablename__ = 'products'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String, nullable=False)
    votesperuser = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    maxvotesperbug = Column(SmallInteger, nullable=False, server_default=text("'10000'"))
    votestoconfirm = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    defaultmilestone = Column(String(64), nullable=False, server_default=text("'---'"))
    classification_id = Column(ForeignKey(u'classifications.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'1'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    allows_unconfirmed = Column(Integer, nullable=False, server_default=text("'1'"))

    classification = relationship(u'Classification')


class ProfileSearch(Base):
    __tablename__ = 'profile_search'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    bug_list = Column(String, nullable=False)
    list_order = Column(String)

    user = relationship(u'Profile')


t_profile_setting = Table(
    'profile_setting', metadata,
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('setting_name', ForeignKey(u'setting.name', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('setting_value', String(32), nullable=False),
    Index('profile_setting_value_unique_idx', 'user_id', 'setting_name', unique=True)
)


class Profile(Base):
    __tablename__ = 'profiles'

    userid = Column(Integer, primary_key=True)
    login_name = Column(String(255), nullable=False, unique=True)
    cryptpassword = Column(String(128))
    realname = Column(String(255), nullable=False, server_default=text("''"))
    disabledtext = Column(String, nullable=False)
    mybugslink = Column(Integer, nullable=False, server_default=text("'1'"))
    extern_id = Column(String(64), unique=True)
    disable_mail = Column(Integer, nullable=False, server_default=text("'0'"))
    is_enabled = Column(Integer, nullable=False, server_default=text("'1'"))
    last_seen_date = Column(DateTime)

    parents = relationship(
        u'Profile',
        secondary='watch',
        primaryjoin=u'Profile.userid == watch.c.watched',
        secondaryjoin=u'Profile.userid == watch.c.watcher'
    )


class ProfilesActivity(Base):
    __tablename__ = 'profiles_activity'

    userid = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    who = Column(ForeignKey(u'profiles.userid', onupdate=u'CASCADE'), nullable=False, index=True)
    profiles_when = Column(DateTime, nullable=False, index=True)
    fieldid = Column(ForeignKey(u'fielddefs.id', onupdate=u'CASCADE'), nullable=False, index=True)
    oldvalue = Column(String)
    newvalue = Column(String)
    id = Column(Integer, primary_key=True)

    fielddef = relationship(u'Fielddef')
    profile = relationship(u'Profile', primaryjoin='ProfilesActivity.userid == Profile.userid')
    profile1 = relationship(u'Profile', primaryjoin='ProfilesActivity.who == Profile.userid')


t_quips = Table(
    'quips', metadata,
    Column('quipid', Integer, nullable=False),
    Column('userid', ForeignKey(u'profiles.userid', ondelete=u'SET NULL', onupdate=u'CASCADE'), index=True),
    Column('quip', String(512), nullable=False),
    Column('approved', Integer, nullable=False, server_default=text("'1'"))
)


class RepPlatform(Base):
    __tablename__ = 'rep_platform'
    __table_args__ = (
        Index('rep_platform_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class Report(Base):
    __tablename__ = 'reports'
    __table_args__ = (
        Index('reports_user_id_idx', 'user_id', 'name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    name = Column(String(64), nullable=False)
    query = Column(String, nullable=False)

    user = relationship(u'Profile')


class Resolution(Base):
    __tablename__ = 'resolution'
    __table_args__ = (
        Index('resolution_sortkey_idx', 'sortkey', 'value'),
    )

    id = Column(SmallInteger, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))
    visibility_value_id = Column(SmallInteger, index=True)


class Series(Base):
    __tablename__ = 'series'
    __table_args__ = (
        Index('series_category_idx', 'category', 'subcategory', 'name', unique=True),
    )

    series_id = Column(Integer, primary_key=True)
    creator = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    category = Column(ForeignKey(u'series_categories.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    subcategory = Column(ForeignKey(u'series_categories.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    frequency = Column(SmallInteger, nullable=False)
    query = Column(String, nullable=False)
    is_public = Column(Integer, nullable=False, server_default=text("'0'"))

    series_category = relationship(u'SeriesCategory', primaryjoin='Series.category == SeriesCategory.id')
    profile = relationship(u'Profile')
    series_category1 = relationship(u'SeriesCategory', primaryjoin='Series.subcategory == SeriesCategory.id')


class SeriesCategory(Base):
    __tablename__ = 'series_categories'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

    groups = relationship(u'Group', secondary='category_group_map')


t_series_data = Table(
    'series_data', metadata,
    Column('series_id', ForeignKey(u'series.series_id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('series_date', DateTime, nullable=False),
    Column('series_value', Integer, nullable=False),
    Index('series_data_series_id_idx', 'series_id', 'series_date', unique=True)
)


class Setting(Base):
    __tablename__ = 'setting'

    name = Column(String(32), primary_key=True)
    default_value = Column(String(32), nullable=False)
    is_enabled = Column(Integer, nullable=False, server_default=text("'1'"))
    subclass = Column(String(32))


t_setting_value = Table(
    'setting_value', metadata,
    Column('name', ForeignKey(u'setting.name', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('value', String(32), nullable=False),
    Column('sortindex', SmallInteger, nullable=False),
    Index('setting_value_nv_unique_idx', 'name', 'value', unique=True),
    Index('setting_value_ns_unique_idx', 'name', 'sortindex', unique=True)
)


t_status_workflow = Table(
    'status_workflow', metadata,
    Column('old_status', ForeignKey(u'bug_status.id', ondelete=u'CASCADE', onupdate=u'CASCADE')),
    Column('new_status', ForeignKey(u'bug_status.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('require_comment', Integer, nullable=False, server_default=text("'0'")),
    Index('status_workflow_idx', 'old_status', 'new_status', unique=True)
)


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        Index('tag_user_id_idx', 'user_id', 'name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    user_id = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)

    user = relationship(u'Profile')


class Token(Base):
    __tablename__ = 'tokens'

    userid = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    issuedate = Column(DateTime, nullable=False)
    token = Column(String(16), primary_key=True)
    tokentype = Column(String(8), nullable=False)
    eventdata = Column(String)

    profile = relationship(u'Profile')


t_ts_error = Table(
    'ts_error', metadata,
    Column('error_time', Integer, nullable=False, index=True),
    Column('jobid', Integer, nullable=False, index=True),
    Column('message', String(255), nullable=False),
    Column('funcid', Integer, nullable=False, server_default=text("'0'")),
    Index('ts_error_funcid_idx', 'funcid', 'error_time')
)


class TsExitstatu(Base):
    __tablename__ = 'ts_exitstatus'

    jobid = Column(Integer, primary_key=True)
    funcid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    status = Column(SmallInteger)
    completion_time = Column(Integer)
    delete_after = Column(Integer, index=True)


class TsFuncmap(Base):
    __tablename__ = 'ts_funcmap'

    funcid = Column(Integer, primary_key=True)
    funcname = Column(String(255), nullable=False, unique=True)


class TsJob(Base):
    __tablename__ = 'ts_job'
    __table_args__ = (
        Index('ts_job_coalesce_idx', 'coalesce', 'funcid'),
        Index('ts_job_funcid_idx', 'funcid', 'uniqkey', unique=True),
        Index('ts_job_run_after_idx', 'run_after', 'funcid')
    )

    jobid = Column(Integer, primary_key=True)
    funcid = Column(Integer, nullable=False)
    arg = Column(LONGBLOB)
    uniqkey = Column(String(255))
    insert_time = Column(Integer)
    run_after = Column(Integer, nullable=False)
    grabbed_until = Column(Integer, nullable=False)
    priority = Column(SmallInteger)
    coalesce = Column(String(255))


t_ts_note = Table(
    'ts_note', metadata,
    Column('jobid', Integer, nullable=False),
    Column('notekey', String(255)),
    Column('value', LONGBLOB),
    Index('ts_note_jobid_idx', 'jobid', 'notekey', unique=True)
)


t_user_group_map = Table(
    'user_group_map', metadata,
    Column('user_id', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('group_id', ForeignKey(u'groups.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('isbless', Integer, nullable=False, server_default=text("'0'")),
    Column('grant_type', Integer, nullable=False, server_default=text("'0'")),
    Index('user_group_map_user_id_idx', 'user_id', 'group_id', 'grant_type', 'isbless', unique=True)
)


class Version(Base):
    __tablename__ = 'versions'
    __table_args__ = (
        Index('versions_product_id_idx', 'product_id', 'value', unique=True),
    )

    value = Column(String(64), nullable=False)
    product_id = Column(ForeignKey(u'products.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    id = Column(Integer, primary_key=True)
    isactive = Column(Integer, nullable=False, server_default=text("'1'"))

    product = relationship(u'Product')


t_votes = Table(
    'votes', metadata,
    Column('who', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Column('bug_id', Integer, nullable=False, index=True),
    Column('vote_count', SmallInteger, nullable=False)
)


t_watch = Table(
    'watch', metadata,
    Column('watcher', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False),
    Column('watched', ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True),
    Index('watch_watcher_idx', 'watcher', 'watched', unique=True)
)


class WhineEvent(Base):
    __tablename__ = 'whine_events'

    id = Column(Integer, primary_key=True)
    owner_userid = Column(ForeignKey(u'profiles.userid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    subject = Column(String(128))
    body = Column(String)
    mailifnobugs = Column(Integer, nullable=False, server_default=text("'0'"))

    profile = relationship(u'Profile')


class WhineQuery(Base):
    __tablename__ = 'whine_queries'

    id = Column(Integer, primary_key=True)
    eventid = Column(ForeignKey(u'whine_events.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    query_name = Column(String(64), nullable=False, server_default=text("''"))
    sortkey = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    onemailperbug = Column(Integer, nullable=False, server_default=text("'0'"))
    title = Column(String(128), nullable=False, server_default=text("''"))

    whine_event = relationship(u'WhineEvent')


class WhineSchedule(Base):
    __tablename__ = 'whine_schedules'

    id = Column(Integer, primary_key=True)
    eventid = Column(ForeignKey(u'whine_events.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    run_day = Column(String(32))
    run_time = Column(String(32))
    run_next = Column(DateTime, index=True)
    mailto = Column(Integer, nullable=False)
    mailto_type = Column(SmallInteger, nullable=False, server_default=text("'0'"))

    whine_event = relationship(u'WhineEvent')
