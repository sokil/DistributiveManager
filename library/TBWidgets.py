from flask import request


def _get_query_with_page(page):
    return 'p=' + str(page)


def pager(paginator, pager_range=5):

    current_page = paginator.get_page()
    total_pages = paginator.get_total_pages()

    # Number of visible pages less than total pages number
    if total_pages <= pager_range * 2:
        first_page_number = 1
        last_page_number = total_pages
        step_backward_page_number = None
        step_forward_page_number = None
    
    # Number of visible pages greater than total pages number
    else:

        first_page_number = current_page - pager_range
        last_page_number = current_page + pager_range
        
        if first_page_number < 1:
            last_page_number = last_page_number - first_page_number + 1
            first_page_number = 1
        elif last_page_number > total_pages:
            first_page_number = first_page_number - last_page_number + total_pages
            last_page_number = total_pages
        
        if first_page_number == 1:
            step_backward_page_number = None
        else:
            step_backward_page_number = first_page_number - pager_range - 1
            if step_backward_page_number < 1:
                step_backward_page_number = 1

        if last_page_number == total_pages:
            step_forward_page_number = None
        else:
            step_forward_page_number = last_page_number + pager_range + 1
            if step_forward_page_number > total_pages:
                step_forward_page_number = total_pages
    
    if total_pages <= 1:
        return ""

    html = '<ul class="pagination">'

    # button "step back"
    if step_backward_page_number:
        html += '<li><a class="previous" href="?%s">&larr;</a></li>' % _get_query_with_page(step_backward_page_number)
    else:
        html += '<li class="previous disabled"><span>&larr;</span></li>'

    # pager range
    for page in range(first_page_number, last_page_number + 1):
        if current_page == page:
            html += '<li class="active"><span>%s<span class="sr-only">(current)</span></span></li>' % page
        else:
            html += '<li ><a href="?%s">%s</a></li>' % (_get_query_with_page(page), page)

    # button "step forward"
    if step_forward_page_number:
        html += '<li class="next"><a href="?%s">&rarr;</a></li>' % _get_query_with_page(step_forward_page_number)
    else:
        html += '<li class="next disabled"><span>&rarr;</span></li>'

    html += '</ul>'

    return html