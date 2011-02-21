package MCP.mod_mcp;

import net.minecraft.src.Material;
import MCP.BlockBase;

public class BlockSilverOre extends BlockBase
{
	/**********************************************************************
	 * 
	 */
	public BlockSilverOre(int id, int textureID, Material material)
	{
		super(id, textureID, material);

		setHardness(3F);
		setResistance(5F);
		setStepSound(soundStoneFootstep);
		setBlockName("silverOre");
	}
}
