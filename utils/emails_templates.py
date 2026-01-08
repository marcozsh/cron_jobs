def get_template(type_account: str, user_name: str, account_number: str, due_date: str, amount: str, payment_link: str = "#") -> str:
    """
    Template HTML para notificación de factura 
    
    Args:
        type_account: Tipo de cuenta (Luz, Gas o Agua)
        user_name: Nombre del usuario
        account_number: Número de cuenta
        due_date: Fecha de vencimiento
        amount: Monto a pagar
        payment_link: URL para realizar el pago
    """
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Factura de {type_account} disponible</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 20px 0; text-align: center; background-color: #f4f4f4;">
                    <table role="presentation" style="width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 40px 20px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">⚡ Factura Disponible</h1>
                            </td>
                        </tr>
                        
                        <!-- Saludo -->
                        <tr>
                            <td style="padding: 30px 40px 20px;">
                                <p style="margin: 0; font-size: 16px; color: #333333; line-height: 1.5;">
                                    Hola <strong>{user_name}</strong>,
                                </p>
                                <p style="margin: 15px 0 0; font-size: 16px; color: #333333; line-height: 1.5;">
                                    Tu factura de {type_account} ya está disponible para consulta y pago.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Detalles de la factura -->
                        <tr>
                            <td style="padding: 20px 40px;">
                                <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f8f9fa; border-radius: 6px; padding: 20px;">
                                    <tr>
                                        <td style="padding: 15px;">
                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                <tr>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #666666;">
                                                        <strong>Número de cuenta:</strong>
                                                    </td>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #333333; text-align: right;">
                                                        {account_number}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #666666; border-top: 1px solid #e0e0e0;">
                                                        <strong>Monto a pagar:</strong>
                                                    </td>
                                                    <td style="padding: 8px 0; font-size: 20px; color: #667eea; text-align: right; font-weight: bold; border-top: 1px solid #e0e0e0;">
                                                        ${amount}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #666666; border-top: 1px solid #e0e0e0;">
                                                        <strong>Fecha de consulta:</strong>
                                                    </td>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #d32f2f; text-align: right; font-weight: bold; border-top: 1px solid #e0e0e0;">
                                                        {due_date}
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Botón de acción -->
                        <tr>
                            <td style="padding: 20px 40px 30px; text-align: center;">
                                <a href="{payment_link}" style="display: inline-block; padding: 14px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: bold; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);">
                                    Ver Factura y Pagar
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return html_template