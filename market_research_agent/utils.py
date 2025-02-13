from composio import ComposioToolSet
def creating_connection(
    entity_id,
    app_name,
    toolset
):
    entity = toolset.get_entity(entity_id);
    collected_params = {}
    expected_params = toolset.get_expected_params_for_user(app=app_name)
    scheme = expected_params['auth_scheme']
    expected_param_names = expected_params['expected_params']
    if scheme=='OAUTH2':
        try:
            connection_details = entity.get_connection(app=app_name.lower()) 
        except:
            connection_details = entity.initiate_connection(app_name=app_name)
            print(f"Please connect your {app_name} account with the following link:{connection_details.redirectUrl}")
            connection_details.wait_until_active(client=toolset.client, timeout=60)
            return connection_details
        print('\n')
        return connection_details
    if scheme=='API_KEY':
        try:
            connection_details = entity.get_connection(app=app_name) 
        except:
            for field in expected_param_names:
                field_value = input(f'For the app {app_name}, Enter the value for {field.name}: ')
                collected_params[field.name]=field_value
            print(collected_params)
            connection_details = toolset.initiate_connection(
                connected_account_params=collected_params,
                app=app_name,
                entity_id=entity_id,
                auth_scheme=scheme
            )
            connection_details.wait_until_active(client=toolset.client, timeout=60)
            return connection_details
        print('\n')
        return connection_details



