package MCP.mod_mcp;

import net.minecraft.src.Material;
import MCP.ApiController;
import MCP.BlockItemBase;

public class ItemSilverOre extends BlockItemBase
{
	/**********************************************************************
	 * 
	 */
	public ItemSilverOre(ApiController ctrl, int textureID, Material material, Class<BlockSilverOre> cls)
	{
		super(ctrl.getBlockItemID(ItemSilverOre.class), textureID, material, cls);
		
		setItemName("silverOre");
	}
}
