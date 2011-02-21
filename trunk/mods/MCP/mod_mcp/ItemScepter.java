package MCP.mod_mcp;

import MCP.ApiController;
import MCP.ItemBase;

public class ItemScepter extends ItemBase
{
	/**********************************************************************
	 * 
	 */
	public ItemScepter(ApiController ctrl, int iconID)
	{
		super(ctrl.getItemID(ItemScepter.class));
		
		setIconIndex(iconID);
		setItemName("scepter");
	}
}
