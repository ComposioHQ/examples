def creating_connection(
    entity_id,
    app_name,
    toolset
):
    entity = toolset.get_entity(entity_id);
    try:
        connection_details = entity.get_connection(app=app_name) 
    except:
        connection_details = entity.initiate_connection(app_name=app_name)
        print(f"Please connect your {app_name} account with the following link:{connection_details.redirectUrl}")
        connection_details.wait_until_active(client=toolset.client, timeout=60)
        return connection_details
    print('\n')
    return connection_details
