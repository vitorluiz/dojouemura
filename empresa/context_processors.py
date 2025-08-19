def empresa_info(request):
    """
    Context processor para disponibilizar informações da empresa
    em todos os templates
    """
    try:
        from .models import Empresa
        empresa = Empresa.objects.filter(ativo=True).first()
        return {'empresa_info': empresa}
    except:
        return {'empresa_info': None}
