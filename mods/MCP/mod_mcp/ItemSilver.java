package MCP.mod_mcp;

import MCP.ApiController;
import MCP.ItemBase;

public class ItemSilver extends ItemBase
{
	/**********************************************************************
	 * 
	 */
	public ItemSilver(ApiController ctrl, int iconID)
	{
		super(ctrl.getItemID(ItemSilver.class));

		setIconIndex(iconID);
		setItemName("silver");
	}
}
