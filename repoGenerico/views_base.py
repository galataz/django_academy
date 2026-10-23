"""Vistas genéricas sobre ORM, para la academia pública."""
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
class BaseListQueryView(APIView):
    model=None
    serializer_class=None
    allowed_ordering=('number',)
    def get_queryset(self):return self.model.objects.all()
    def apply_search(self,queryset,search):return queryset
    def get(self,request):
        try:
            page=int(request.query_params.get('page',1))
            size=int(request.query_params.get('per_page',10))
        except (TypeError,ValueError):return Response({'success':False,'error':'Paginación inválida.'},status=400)
        if page<1 or not 1<=size<=100:return Response({'success':False,'error':'page >= 1; per_page entre 1 y 100.'},status=400)
        ordering=request.query_params.get('ordering','number')
        if ordering.lstrip('-') not in self.allowed_ordering:return Response({'success':False,'error':'Orden no permitido.'},status=400)
        queryset=self.apply_search(self.get_queryset(),request.query_params.get('search','')[:200]).order_by(ordering)
        paginator=Paginator(queryset,size)
        result=paginator.get_page(page)
        return Response({'success':True,'results':self.serializer_class(result.object_list,many=True).data,'total_count':paginator.count,'current_page':result.number,'total_pages':paginator.num_pages})
