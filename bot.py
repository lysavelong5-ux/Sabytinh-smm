async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    original_caption = query.message.caption or ""
    
    if data.startswith("approve_"):
        target_user_id = int(data.split("_")[1])
        await query.edit_message_caption(caption=original_caption + "\n\nStatus: Approved ✅", parse_mode="Markdown")
        try: 
            await context.bot.send_message(chat_id=target_user_id, text="Your order has been Approved! ✅")
        except: pass
        
    elif data.startswith("reject_"):
        target_user_id = int(data.split("_")[1])
        await query.edit_message_caption(caption=original_caption + "\n\nStatus: Rejected ❌", parse_mode="Markdown")
        try: 
            await context.bot.send_message(chat_id=target_user_id, text="Your order has been Rejected. ❌")
        except: pass
        
    elif data.startswith("fundapprove_"):
        # ទម្រង់: fundapprove_user_id_amount
        parts = data.split("_")
        target_user_id = int(parts[1])
        amount = float(parts[2])
        
        user_balances[target_user_id] = user_balances.get(target_user_id, 0.00) + amount
        await query.edit_message_caption(caption=original_caption + f"\n\nStatus: Approved ✅ (+${amount:.2f})", parse_mode="Markdown")
        try: 
            await context.bot.send_message(
                chat_id=target_user_id, 
                text=f"🎉 Admin approved your top-up of **${amount:.2f}**!\n💰 Balance: **${user_balances[target_user_id]:.2f}**", 
                parse_mode="Markdown"
            )
        except: pass
        
    elif data.startswith("fundreject_"):
        target_user_id = int(data.split("_")[1])
        await query.edit_message_caption(caption=original_caption + "\n\nStatus: Rejected ❌", parse_mode="Markdown")
        try: 
            await context.bot.send_message(chat_id=target_user_id, text="❌ Top-up request rejected.")
        except: pass
