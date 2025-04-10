from sqlalchemy import func

def moreFilter(request):
    r = []
    search = request.query_params.get("search", "")
    if(search):
        r.append("search="+search)

    limit = request.query_params.get("limit", "")
    if(limit):
        r.append("limit="+limit)

    return ("&" if len(r) > 0 else "")+"&".join(r)
    

def getPagination(query, request):
    page = request.query_params.get("page", 1)
    limit = request.query_params.get("limit", 10)

    try:
        current_page = int(page)
    except ValueError:
        current_page = 1

    try:
        limit = int(limit)
    except ValueError:
        limit = 1

    # Calcular o offset com base na página e no limite
    offset = (current_page - 1) * limit
    
    # Consultar os medicamentos paginados
    data = query.offset(offset).limit(limit).all()
    
    # Calcular o número total de medicamentos
    total_clients = query.count()
    
    # Calcular o número total de páginas
    total_pages = (total_clients // limit) + (1 if total_clients % limit > 0 else 0)

    first_page = 1
    last_page = total_pages

    start_page = current_page - 2 if current_page - 2 > first_page else first_page
    end_page = current_page + 2 if current_page + 2 < last_page else last_page

    return (
        data, 
        {
            "current_page": current_page,
            "total_pages": total_pages,
            "first_page": first_page,
            "last_page": last_page,
            "start_page": start_page,
            "end_page": end_page,
            "limit": limit,
            "more_filter": moreFilter(request)
        } 
    )