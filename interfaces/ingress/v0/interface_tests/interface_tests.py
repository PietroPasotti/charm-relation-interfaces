from scenario.structs import State, relation
from interface_test import InterfaceTestCase


class IngressProviderTestCreated(InterfaceTestCase):
    EVENT = 'ingress-relation-created'
    INPUT_STATE = State()
    ROLE = 'provider'

    # nothing happens on created

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_app_data
        assert not relation.local_unit_data


class IngressProviderTestJoined(InterfaceTestCase):
    EVENT = 'ingress-relation-joined'
    INPUT_STATE = State()
    ROLE = 'provider'

    # nothing happens on joined

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_app_data
        assert not relation.local_unit_data


class IngressProviderTestChangedValid(InterfaceTestCase):
    EVENT = 'ingress-relation-changed'
    INPUT_STATE = State(
        relations=[relation(
            # todo: endpoint is unknown/overwritten: find an elegant way to omit it here.
            #  perhaps input state is too general: we only need this relation meta:
            endpoint='ingress',
            interface='ingress',
            remote_app_name='remote',
            remote_units_data={0: {
                'host': '0.0.0.42',
                'model': 'bar',
                'name': 'baz',
                'port': '42',
            }}
        )]
    )
    ROLE = 'provider'

    # on changed, if the remote side has sent valid data: our side is populated.

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_unit_data
        assert relation.local_app_data


class IngressProviderTestChangedInvalid(InterfaceTestCase):
    EVENT = 'ingress-relation-changed'
    INPUT_STATE = State(relations=[relation(
            # todo: endpoint is unknown/overwritten: find an elegant way to omit it here.
            #  perhaps input state is too general: we only need this relation meta:
            endpoint='ingress',
            interface='ingress',
            remote_app_name='remote',
            remote_units_data={0: {
                'port': '42',
                'bubble': 'rubble'
            }}
        )]
    )

    ROLE = 'provider'

    # on changed, if the remote side has sent INvalid data: local side didn't publish anything either.

    @staticmethod
    def validate(output_state: State):
        relation = output_state.relations[0]
        assert not relation.local_app_data
        assert not relation.local_unit_data



class IngressRequirerTest(InterfaceTestCase):
    EVENT = 'ingress-relation-changed'
    ROLE = 'requirer'

    def validate(self, output_state: State):
        pass